frappe.pages['gym_navigation'].on_page_load = function (wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: '🏋️ Gym Management Dashboard',
        single_column: true
    });

    const userRoles = frappe.user_roles || [];

    const modules = [
        { name: "Gym Trainer", icon: "🧑‍🏫", roles: ["Gym Admin"] },
        { name: "Gym Member", icon: "🧍‍♂️", roles: ["Gym Admin"] },
        { name: "Fitness Tracker", icon: "📈", roles: ["Gym Member", "Gym Trainer", "Gym Admin"] },
        { name: "Gym Membership", icon: "🎫", roles: ["Gym Admin", "Gym Member"] },
        { name: "Gym Workout Plan", icon: "📝", roles: ["Gym Admin", "Gym Trainer"] },
        { name: "Gym Setting", icon: "⚙️", roles: ["Gym Admin"] },
        { name: "Gym Locker Booking", icon: "🔐", roles: ["Gym Admin", "Gym Member"] },
        { name: "Gym Class Booking", icon: "📅", roles: ["Gym Admin", "Gym Member"] },
        { name: "Gym Trainer Subscription", icon: "💳", roles: ["Gym Admin", "Gym Member"] }
    ];

    const allowedModules = modules;

    $(page.body).html(`
      <div class="gym-header">
        <div class="gym-header-left">
            <h2>Welcome, ${frappe.session.user_fullname || frappe.session.user}</h2>
            ${(userRoles.includes("Gym Member") || userRoles.includes("Gym Trainer")) && !userRoles.includes("Gym Admin") ? `
                <button id="viewProfile" class="btn btn-primary btn-sm mt-2">👤 View My Profile</button>
            ` : ''}
        </div>
        <div class="gym-actions">
            <input type="text" id="searchBox" class="form-control" placeholder="Search modules..." />
            <button id="toggleMode" class="btn btn-outline-secondary">🌙 Dark Mode</button>
        </div>
      </div>

      <div class="gym-stats">
        <div class="stat-box">👥 Members<br><span id="stat-members">...</span></div>
        <div class="stat-box">🏋️ Trainers<br><span id="stat-trainers">...</span></div>
        <div class="stat-box">🔐 Lockers Today<br><span id="stat-lockers">...</span></div>
        <div class="stat-box">📅 Class Bookings<br><span id="stat-classes">...</span></div>
      </div>

      <div class="gym-dashboard-container">
        ${allowedModules.map(m => {
            const slug = frappe.router.slug(m.name);
            return `
                <div class="gym-card" data-name="${m.name.toLowerCase()}">
                    <a href="/app/${slug}">
                        <div class="gym-card-content">
                            <div class="gym-icon">${m.icon}</div>
                            <h4>${m.name}</h4>
                        </div>
                    </a>
                </div>
            `;
        }).join("")}
      </div>

      <style>
        .gym-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 25px;
        }

        .gym-header h2 {
            font-weight: bold;
            color: #444;
            margin-bottom: 10px;
        }

        .gym-actions {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        .form-control {
            padding: 8px 12px;
            min-width: 250px;
        }

        .gym-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-box {
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            padding: 20px;
            text-align: center;
            font-size: 1rem;
            font-weight: 600;
            color: #444;
            transition: all 0.3s ease-in-out;
        }

        .stat-box span {
            display: block;
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 5px;
            color: #222;
        }

        .gym-dashboard-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            justify-items: center;
            align-items: stretch;
            padding: 10px;
        }

        .gym-card {
            width: 100%;
            max-width: 250px;
            height: 180px;
            background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
            border-radius: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            transition: transform 0.4s ease, box-shadow 0.4s ease;
            cursor: pointer;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .gym-card:hover {
            transform: translateY(-8px) scale(1.03);
            box-shadow: 0 20px 30px rgba(0,0,0,0.2);
        }

        .gym-card a {
            text-decoration: none;
            color: inherit;
            display: block;
            padding: 35px 20px;
            width: 100%;
            height: 100%;
        }

        .gym-icon {
            font-size: 2.8rem;
            margin-bottom: 10px;
        }

        .gym-card-content h4 {
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0;
        }

        body.dark-mode {
            background-color: #1e1e2f;
            color: #eee;
        }

        body.dark-mode .gym-card {
            background: linear-gradient(135deg, #434343 0%, #000000 100%);
            color: #fff;
        }

        body.dark-mode .stat-box {
            background: #2a2a3a;
            color: #eee;
        }

        body.dark-mode .stat-box span {
            color: #fff;
        }

        body.dark-mode input,
        body.dark-mode .form-control {
            background-color: #333;
            color: #eee;
            border: 1px solid #555;
        }

        body.dark-mode .btn-outline-secondary {
            border-color: #aaa;
            color: #eee;
        }
      </style>
    `);

    // 🌙 Dark mode toggle
    $("#toggleMode").on("click", () => {
        $("body").toggleClass("dark-mode");
        const modeText = $("body").hasClass("dark-mode") ? "☀️ Light Mode" : "🌙 Dark Mode";
        $("#toggleMode").text(modeText);
    });

    // 🔍 Search filter
    $("#searchBox").on("input", function () {
        const term = $(this).val().toLowerCase();
        $(".gym-card").each(function () {
            const name = $(this).data("name");
            $(this).toggle(name.includes(term));
        });
    });

    // 👤 View Profile shortcut (only for Gym Member / Trainer, not Admin)
    $("#viewProfile").on("click", function () {
        frappe.call({
            method: 'gym_management.gym_management.page.member_profile_1.member_profile_1.get_member_profile',
            callback: function (r) {
                if (r.message) {
                    frappe.set_route("member-profile-1");
                } else {
                    frappe.msgprint("Could not load your profile. Please contact admin.");
                }
            }
        });
    });

    // 📊 Real-time stats fetch
    frappe.call({
        method: "gym_management.services.api.get_dashboard_stats",
        callback: function (r) {
            if (r.message) {
                const stats = r.message;
                $("#stat-members").text(stats.active_members);
                $("#stat-trainers").text(stats.active_trainers);
                $("#stat-lockers").text(stats.lockers_today);
                $("#stat-classes").text(stats.class_bookings_today);
            }
        }
    });
};

