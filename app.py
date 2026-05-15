import os
import bcrypt

from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from Connection.db_connection import connect

from Models.Roles import Roles
from Models.Users import Users
from Models.Guests import Guests
from Models.RoomTypes import RoomTypes
from Models.Rooms import Rooms
from Models.Bookings import Bookings
from Models.Stays import Stays
from Models.Services import Services
from Models.BookingServices import BookingServices
from Models.CleaningTasks import CleaningTasks

from Controllers.RolesController import RolesController
from Controllers.UsersController import UsersController
from Controllers.GuestsController import GuestsController
from Controllers.RoomTypesController import RoomTypesController
from Controllers.RoomsController import RoomsController
from Controllers.BookingsController import BookingsController
from Controllers.StaysController import StaysController
from Controllers.ServicesController import ServicesController
from Controllers.BookingServicesController import BookingServicesController
from Controllers.CleaningTasksController import CleaningTasksController

application = Flask(__name__, template_folder="templates", static_folder="static")
application.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

login_manager = LoginManager(application)
login_manager.login_view = "login_page"


@login_manager.user_loader
def user_loader(user_id):
    """Подгружает пользователя по id из cookie-сессии."""
    return UsersController.show(int(user_id))

def init_db():
    """Создаёт таблицы, базовые роли и тестовых пользователей."""
    db = connect()
    db.connect(reuse_if_open=True)

    tables = [
        Roles,
        Users,
        Guests,
        RoomTypes,
        Rooms,
        Bookings,
        Stays,
        Services,
        BookingServices,
        CleaningTasks,
    ]
    db.create_tables(tables, safe=True)

    # Роли на русском
    roles_map = {
        1: "Администратор",
        2: "Горничная",
        3: "Управляющий",
        4: "Гость",
    }
    for rid, rname in roles_map.items():
        role = Roles.get_or_none(Roles.id == rid)
        if role is None:
            Roles.create(id=rid, name=rname)
            print(f"[INFO] Создана роль: {rname}")

    # Администратор
    admin = Users.get_or_none(Users.username == "admin")
    if admin is None:
        admin = UsersController.add(
            username="admin",
            email="admin@hotel.com",
            password="admin123",
            role_id=1,
            first_name="Администратор",
            last_name="Системы"
        )
        print("[INFO] Создан администратор: admin / admin123")

    # Горничная
    maid = Users.get_or_none(Users.username == "maid")
    if maid is None:
        maid = UsersController.add(
            username="maid",
            email="maid@hotel.com",
            password="maid123",
            role_id=2,
            first_name="Горничная",
            last_name="Служба"
        )
        print("[INFO] Создана горничная: maid / maid123")

    # Гость (с телефоном для поиска)
    guest_user = Users.get_or_none(Users.username == "guest")
    if guest_user is None:
        guest_user = UsersController.add(
            username="guest",
            email="guest@example.com",
            password="guest123",
            role_id=4,
            first_name="Тестовый",
            last_name="Гость",
            phone="+79991234567"
        )
        GuestsController.create(guest_user.id, passport_number="", preferences="")
        print("[INFO] Создан тестовый гость: guest / guest123 / тел: +79991234567")

    # Типы номеров
    if RoomTypes.select().count() == 0:
        RoomTypes.create(name="Стандарт", base_price=3000.00)
        RoomTypes.create(name="Люкс", base_price=8000.00)
        RoomTypes.create(name="Полулюкс", base_price=5000.00)
        RoomTypes.create(name="Семейный", base_price=6000.00)
        print("[INFO] Созданы типы номеров")

    # Услуги
    if Services.select().count() == 0:
        Services.create(name="Завтрак", price=500.00, category="meal")
        Services.create(name="Обед", price=700.00, category="meal")
        Services.create(name="Ужин", price=800.00, category="meal")
        Services.create(name="Спа-процедура", price=2500.00, category="spa")
        Services.create(name="Трансфер из аэропорта", price=1500.00, category="transfer")
        print("[INFO] Созданы услуги")

    # Тестовые номера
    if Rooms.select().count() == 0:
        Rooms.create(room_number="101", room_type_id=1, capacity=2, status="available")
        Rooms.create(room_number="102", room_type_id=1, capacity=2, status="available")
        Rooms.create(room_number="201", room_type_id=2, capacity=4, status="available")
        Rooms.create(room_number="202", room_type_id=3, capacity=3, status="available")
        print("[INFO] Созданы тестовые номера")

    db.close()
    print("[INFO] Инициализация базы данных завершена")

def current_user_role():
    if not current_user.is_authenticated:
        return None
    role = current_user.role
    return role.name if role else None


def is_admin():
    return current_user.is_authenticated and current_user.role.name == "Администратор"


def is_maid():
    return current_user.is_authenticated and current_user.role.name == "Горничная"


def is_manager():
    return current_user.is_authenticated and current_user.role.name == "Управляющий"


def is_guest():
    return current_user.is_authenticated and current_user.role.name == "Гость"


def current_guest():
    if not current_user.is_authenticated or current_user.role.name != "Гость":
        return None
    return GuestsController.show_by_user_id(current_user.id)

@application.route("/", methods=["GET"])
def home():
    room_types = RoomTypesController.get()
    return render_template("index.html", room_types=room_types)


@application.route("/login", methods=["GET", "POST"])
def login_page():
    message = ""
    if request.method == "POST":
        login = request.form.get("login", "").strip()
        password = request.form.get("password", "")

        user = UsersController.auth(login, password)
        if user:
            login_user(user)
            return redirect("/dashboard")

        message = "Неверный логин или пароль"

    return render_template("login.html", message=message)


@application.route("/register", methods=["GET", "POST"])
def register_page():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")
        first_name = request.form.get("first_name", "")
        last_name = request.form.get("last_name", "")
        phone = request.form.get("phone", "")

        if not all([username, email, password, password2]):
            message = "Заполните все поля"
            return render_template("register.html", message=message)

        if password != password2:
            message = "Пароли не совпадают"
            return render_template("register.html", message=message)

        if UsersController.show_login(username):
            message = "Пользователь с таким username уже существует"
            return render_template("register.html", message=message)

        if UsersController.show_login(email):
            message = "Пользователь с таким email уже существует"
            return render_template("register.html", message=message)

        user = UsersController.add(
            username=username,
            email=email,
            password=password,
            role_id=4,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        if user:
            GuestsController.create(user.id, passport_number="", preferences="")
            return redirect("/login")

        message = "Ошибка регистрации"

    return render_template("register.html", message=message)


@application.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/")

@application.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    role = current_user_role()

    rooms = RoomsController.get()
    room_types = RoomTypesController.get()
    all_bookings = BookingsController.get()
    active_stays = StaysController.get_active()
    cleaning_tasks = CleaningTasksController.get_pending()

    # Бронирования для гостя
    guest_bookings = []
    if role == "Гость":
        guest = current_guest()
        if guest:
            guest_bookings = BookingsController.get_by_guest(guest.id)

    active_stays_data = []
    for stay in active_stays:
        active_stays_data.append({
            'id': stay.id,
            'guest_name': stay.guest.user.get_full_name() if stay.guest and stay.guest.user else "—",
            'room_number': stay.room.room_number if stay.room else "—",
            'check_in_time': stay.check_in_time.strftime("%d.%m.%Y %H:%M") if stay.check_in_time else "—"
        })

    return render_template(
        "dashboard.html",
        role=role,
        rooms=rooms,
        room_types=room_types,
        bookings=guest_bookings,
        all_bookings=all_bookings,
        active_stays=active_stays_data,
        cleaning_tasks=cleaning_tasks
    )

@application.route("/book_room", methods=["GET", "POST"])
@login_required
def book_room():
    if not is_guest():
        flash("Только для гостей", "error")
        return redirect("/dashboard")

    guest = current_guest()
    if not guest:
        flash("Профиль гостя не найден", "error")
        return redirect("/dashboard")

    if request.method == "POST":
        room_id = request.form.get("room_id")
        check_in = request.form.get("check_in_date")
        check_out = request.form.get("check_out_date")

        if not room_id:
            flash("Выберите номер", "error")
            return redirect("/book_room")

        if not check_in or not check_out:
            flash("Укажите даты заезда и выезда", "error")
            return redirect("/book_room")

        room = RoomsController.show(int(room_id))
        if not room:
            flash("Номер не найден", "error")
            return redirect("/book_room")

        if room.status != "available":
            flash(f"Номер {room.room_number} недоступен для бронирования", "error")
            return redirect("/book_room")

        from datetime import datetime
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

        if check_in_date >= check_out_date:
            flash("Дата выезда должна быть позже даты заезда", "error")
            return redirect("/book_room")

        # Проверка на пересечение бронирований
        if not BookingsController.is_room_available(room.id, check_in, check_out):
            flash(f"Номер {room.room_number} уже забронирован на выбранные даты", "error")
            return redirect("/book_room")

        nights = (check_out_date - check_in_date).days
        total_price = nights * room.room_type.base_price

        booking = BookingsController.create(
            guest.id,
            room.id,
            check_in,
            check_out,
            total_price
        )

        if booking:
            flash(f"Номер {room.room_number} забронирован! Стоимость: {total_price} ₽", "success")
            return redirect("/dashboard")
        else:
            flash("Ошибка при создании бронирования", "error")
            return redirect("/book_room")

    rooms = RoomsController.get_available()
    return render_template("book_room.html", rooms=rooms)

@application.route("/rooms", methods=["GET"])
@login_required
def rooms_page():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    rooms = RoomsController.get()
    room_types = RoomTypesController.get()
    return render_template("rooms.html", rooms=rooms, room_types=room_types)


@application.route("/rooms/create", methods=["POST"])
@login_required
def create_room():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    room_number = request.form.get("room_number")
    room_type_id = request.form.get("room_type_id")
    capacity = request.form.get("capacity")

    RoomsController.create(room_number, int(room_type_id), int(capacity))
    flash("Номер добавлен", "success")
    return redirect("/rooms")


@application.route("/rooms/<int:room_id>/status", methods=["POST"])
@login_required
def update_room_status(room_id):
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    status = request.form.get("status")
    old_room = RoomsController.show(room_id)
    old_status = old_room.status if old_room else None

    RoomsController.update_status(room_id, status)

    # Если новый статус "cleaning" — создаём задание на уборку
    if status == "cleaning":
        existing_task = CleaningTasks.select().where(
            (CleaningTasks.room_id == room_id) & (CleaningTasks.status == "pending")
        ).first()
        if existing_task:
            flash("Статус номера обновлён, задание на уборку уже существует", "info")
        else:
            task = CleaningTasksController.create(room_id)
            if task:
                flash("Статус номера обновлён, задание на уборку создано", "success")
            else:
                flash("Статус номера обновлён, но задание не создалось", "warning")
    else:
        flash("Статус номера обновлён", "success")

    return redirect("/rooms")


@application.route("/rooms/api", methods=["GET"])
@login_required
def rooms_api():
    if not is_admin():
        return jsonify({"error": "Доступ запрещён"}), 403

    rooms = RoomsController.get()
    result = []
    for r in rooms:
        result.append({
            'id': r.id,
            'room_number': r.room_number,
            'room_type': r.room_type.name if r.room_type else "—",
            'status': r.status
        })
    return jsonify(result)

@application.route("/bookings", methods=["GET"])
@login_required
def bookings_page():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    bookings = BookingsController.get()
    return render_template("bookings.html", bookings=bookings)


@application.route("/bookings/create", methods=["POST"])
@login_required
def create_booking():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    guest_id = request.form.get("guest_id")
    room_id = request.form.get("room_id")
    check_in = request.form.get("check_in_date")
    check_out = request.form.get("check_out_date")
    total_price = request.form.get("total_price")

    # Проверка на пересечение бронирований
    if not BookingsController.is_room_available(int(room_id), check_in, check_out):
        flash("Номер уже забронирован на выбранные даты", "error")
        return redirect("/bookings")

    BookingsController.create(
        int(guest_id), int(room_id), check_in, check_out, float(total_price)
    )
    flash("Бронирование создано", "success")
    return redirect("/bookings")


@application.route("/bookings/search", methods=["GET"])
@login_required
def search_bookings():
    if not is_admin():
        return jsonify({"error": "Доступ запрещён"}), 403

    phone = request.args.get("phone")
    if not phone:
        return jsonify({"bookings": []})

    bookings = BookingsController.search_by_phone(phone)
    result = []
    for b in bookings:
        result.append({
            'id': b.id,
            'guest_name': b.guest.user.get_full_name() if b.guest and b.guest.user else "—",
            'guest_phone': b.guest.user.phone if b.guest and b.guest.user else "—",
            'room_number': b.room.room_number if b.room else "—",
            'check_in': str(b.check_in_date),
            'check_out': str(b.check_out_date),
            'status': b.status
        })
    return jsonify({"bookings": result})

@application.route("/checkin", methods=["GET"])
@login_required
def checkin_page():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    confirmed_bookings = Bookings.select().where(Bookings.status == "confirmed")
    available_rooms = RoomsController.get_available()

    return render_template("checkin.html", confirmed_bookings=confirmed_bookings, available_rooms=available_rooms)


@application.route("/checkin/do", methods=["POST"])
@login_required
def do_checkin():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    booking_id = request.form.get("booking_id")
    room_id = request.form.get("room_id")

    if not booking_id or not room_id:
        flash("Выберите бронирование и номер", "error")
        return redirect("/checkin")

    booking = BookingsController.show(int(booking_id))
    if not booking or booking.status != "confirmed":
        flash("Бронирование не найдено или не подтверждено", "error")
        return redirect("/checkin")

    room = RoomsController.show(int(room_id))
    if not room or room.status != "available":
        flash("Номер недоступен", "error")
        return redirect("/checkin")

    # Обновляем статус номера
    RoomsController.update_status(room.id, "occupied")

    # Обновляем статус бронирования
    BookingsController.update_status(booking.id, "checked_in")

    # Создаём запись о проживании
    StaysController.create(booking.id, booking.guest_id, room.id, booking.total_price)

    flash("Заезд выполнен успешно", "success")
    return redirect("/dashboard")

@application.route("/checkout/api", methods=["GET"])
@login_required
def checkout_api():
    """API для получения списка активных проживаний."""
    if not is_admin():
        return jsonify({"error": "Доступ запрещён"}), 403

    active_stays = StaysController.get_active()
    result = []
    for stay in active_stays:
        result.append({
            'id': stay.id,
            'guest_name': stay.guest.user.get_full_name() if stay.guest and stay.guest.user else "—",
            'room_number': stay.room.room_number if stay.room else "—",
            'check_in_time': stay.check_in_time.strftime("%d.%m.%Y %H:%M") if stay.check_in_time else "—",
            'total_amount': float(stay.total_amount) if stay.total_amount else 0
        })
    return jsonify({"stays": result})


@application.route("/checkout", methods=["GET"])
@login_required
def checkout_page():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    active_stays = StaysController.get_active()
    active_stays_data = []
    for stay in active_stays:
        active_stays_data.append({
            'id': stay.id,
            'guest_name': stay.guest.user.get_full_name() if stay.guest and stay.guest.user else "—",
            'room_number': stay.room.room_number if stay.room else "—",
            'check_in_time': stay.check_in_time.strftime("%d.%m.%Y %H:%M") if stay.check_in_time else "—"
        })

    return render_template("checkout.html", active_stays=active_stays_data)


@application.route("/checkout/do", methods=["POST"])
@login_required
def do_checkout():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    stay_id = request.form.get("stay_id")
    if not stay_id:
        flash("Не указано проживание", "error")
        return redirect("/checkout")

    stay = StaysController.show(int(stay_id))
    if not stay or stay.check_out_time:
        flash("Проживание не найдено или уже завершено", "error")
        return redirect("/checkout")

    # Обновляем время выезда
    StaysController.checkout(stay.id)

    # Обновляем статус бронирования
    booking = stay.booking
    BookingsController.update_status(booking.id, "checked_out")

    # Обновляем статус номера
    room = stay.room
    RoomsController.update_status(room.id, "cleaning")

    # Создаём задание на уборку
    CleaningTasksController.create(room.id)

    flash("Выезд выполнен успешно", "success")
    return redirect("/dashboard")

@application.route("/cleaning", methods=["GET"])
@login_required
def cleaning_page():
    if not is_maid() and not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    tasks = CleaningTasksController.get_pending()
    return render_template("cleaning.html", tasks=tasks)


@application.route("/cleaning/<int:task_id>/complete", methods=["POST"])
@login_required
def complete_cleaning(task_id):
    if not is_maid() and not is_admin():
        flash("Доступ запрещён", "error")
        return redirect("/dashboard")

    task = CleaningTasksController.complete(task_id)
    if task:
        room = task.room
        RoomsController.update_status(room.id, "available")
        flash("Уборка завершена", "success")
    else:
        flash("Задание не найдено или уже выполнено", "error")

    return redirect("/cleaning")

app = application

if __name__ == "__main__":
    init_db()
    application.run(debug=True, host="0.0.0.0", port=5000)