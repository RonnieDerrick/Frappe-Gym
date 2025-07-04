frappe.pages['member-profile-1'].on_page_load = function(wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Member Profile',
		single_column: true
	});

	$(wrapper).html(`
		<style>
			.profile-container {
				padding: 20px;
				display: grid;
				grid-template-columns: 1fr;
				gap: 20px;
			}
			.card {
				background: #fff;
				border: 1px solid #e0e0e0;
				border-radius: 12px;
				box-shadow: 0 2px 8px rgba(0,0,0,0.05);
				padding: 20px;
			}
			.card h3 {
				margin-top: 0;
				color: #2b4a77;
			}
			.card p {
				margin: 5px 0;
			}
			.remaining-days {
				background: #f0f9ff;
				border-left: 5px solid #1890ff;
				padding: 10px;
				font-size: 16px;
				font-weight: bold;
				color: #004085;
				border-radius: 8px;
			}
			.profile-block {
				display: flex;
				align-items: center;
				gap: 20px;
			}
			.profile-img {
				width: 100px;
				height: 100px;
				border-radius: 50%;
				object-fit: cover;
				border: 2px solid #ccc;
			}
		</style>

		<div class="profile-container" id="member-profile-content">
			<!-- Dynamic content goes here -->
		</div>
	`);

	frappe.call({
		method: 'gym_management.gym_management.page.member_profile_1.member_profile_1.get_member_profile',
		callback: function(r) {
			if (r.message) {
				const { member, membership, trainer, remaining_days } = r.message;

				// Default photos (if not available)
				const memberPhoto = member.photo || "https://www.w3schools.com/howto/img_avatar.png";
				const trainerPhoto = trainer.photo || "https://www.w3schools.com/howto/img_avatar2.png";

				const content = `
					<div class="card">
						<div class="profile-block">
							<img src="${memberPhoto}" alt="Member Photo" class="profile-img">
							<div>
								<h3>Member Information</h3>
								<p><strong>Name:</strong> ${member.full_name}</p>
							</div>
						</div>
					</div>

					<div class="card">
						<h3>Membership Details</h3>
						<p><strong>Type:</strong> ${membership.membership_type}</p>
						<p><strong>End Date:</strong> ${membership.end_date}</p>
						<div class="remaining-days">🕒 Remaining Days: ${remaining_days}</div>
					</div>

					<div class="card">
						<div class="profile-block">
							<img src="${trainerPhoto}" alt="Trainer Photo" class="profile-img">
							<div>
								<h3>Assigned Trainer</h3>
								<p><strong>Name:</strong> ${trainer.full_name}</p>
								<p><strong>Email:</strong> ${trainer.email}</p>
								<p><strong>Phone:</strong> ${trainer.phone_number}</p>
							</div>
						</div>
					</div>
				`;

				
				$('#member-profile-content').html(content);
			}
		}
	});
};
