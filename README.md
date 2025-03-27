# **📖 README - American University of Nigeria Residence Management System (AUNRMS)**  

## **🚀 Project Overview**  

The **American University of Nigeria Residence Management System (AUNRMS)** is a **🌐 web-based application** designed to streamline and enhance the management of student residences at AUN. The system tackles inefficiencies in traditional residence management by improving **📢 communication**, **⚙️ automating tasks**, and enabling **📊 data-driven decisions**.  

### **✨ Key Features**  
- **👥 User Management**: Account creation, login, and **🔑 role-based access** (residents, RAs, RDs, admins).
- **👨‍💼 Staff Assignment: RAs/RDs can ✅ assign maintenance tasks to specific staff members based on expertise/availability.
- **🏠 Room Assignment & Management: Admins/RDs can 🔀 assign rooms to students, track occupancy status (✅ Occupied, 🚫 Unoccupied, ⚠️ Unavailable), and manage dormitory info.
- **🔧 Maintenance Requests**: Submit, track, and get **🔄 real-time updates** on requests.  
- **📦 Storage Unit Management**: Request storage & manage allocations.  
- **📢 Announcements & Messaging**: Secure **💬 messaging** and announcements for residents/groups.  
- **📈 Reporting & Analytics**: **📊 Automated reports** on maintenance trends, response times, and demographics.  
- **💳 Payment Integration**: Pay residence fees **💸 online**.  
- **🗣️ Anonymous Complaints**: Submit and track complaints **🕵️ anonymously**.
- 
  

---

## **🛠️ Technologies Used**  

### **🔙 Backend**  
- **🖥️ Framework**: Django  
- **🗃️ Database**: PostgreSQL  
- **📊 Data Visualization**: Bokeh, Seaborn  
- **⚡ Real-time Updates**: Ajax, Websockets  

### **🖥️ Frontend**  
- **📜 Languages**: HTML, CSS, JavaScript  
- **🎨 UI Framework**: Bootstrap  
- **✏️ Design Tool**: Figma  

### **🧰 Development Tools**  
- **🔄 Version Control**: Git & GitHub  
- **💻 IDE**: Visual Studio Code  
- **🗄️ Database Management**: pgAdmin  
- **📐 Diagramming**: Draw.io  

---

## **⚙️ System Requirements**  

### **💾 Hardware**  
- **🖥️ Server**: Multi-core CPU, 8GB RAM, SSD storage.  
- **🗄️ Database Server**: Same as server specs.  
- **📱 Client Devices**: Laptops, phones, desktops, tablets, or browsers.  

### **🖥️ Software**  
- **🔙 Backend**: Django, PostgreSQL, Bokeh, Seaborn.  
- **🖼️ Frontend**: HTML, CSS, JavaScript, Bootstrap.  
- **🔧 Tools**: Datepicker.js, Git, VS Code, pgAdmin.  

---

## **🔧 Installation & Setup**  

1. **📥 Clone the Repo**:  
   ```bash
   git clone [repository-url]  
   ```  

2. **📦 Install Dependencies**:  
   ```bash
   pip install -r requirements.txt  
   ```  

3. **🗃️ Database Setup**:  
   - Configure PostgreSQL in `settings.py`.  
   - Run migrations:  
     ```bash
     python manage.py migrate  
     ```  

4. **🚀 Run the App**:  
   ```bash
   python manage.py runserver  
   ```  

5. **🌍 Access the App**:  
   Open `http://localhost:8000` in a browser.  

---

## **👨‍💻 Usage**  

### **🎓 For Residents**  
- Submit **🔧 maintenance requests**, request **📦 storage**, view **📢 announcements**, and track requests.  
- Pay **💳 residence fees** online.  

### **👔 For RAs & RDs**  
- Manage **🔧 requests**, assign **⚠️ severity levels**, update **🔄 statuses**.  
- Send **📢 announcements**, manage **📦 storage**, and generate **📊 reports**.  

### **👑 For Admins**  
- Full **🛠️ admin control** over users, requests, and system settings.  
- Send **📢 announcements** and monitor **📈 system performance**.  

---

## **📌 Methodology (Agile 🏃‍♂️)**  
1. **📝 Planning**: Gather requirements & feedback.  
2. **📊 Analysis & Design**: Define logic & architecture.  
3. **👨‍💻 Implementation**: Build the system.  
4. **🧪 Testing**: QA & bug fixes.  
5. **🔄 Evaluation**: Review & iterate.  

---

## **⚠️ Challenges & Limitations**  
1. **🔄 Adoption & Training**: Users may need time to adapt.  
2. **🌐 Internet Dependency**: Requires stable connection.  
3. **🔗 Integration**: Compatibility with existing systems.  
4. **💰 Budget Constraints**: May affect quality.  

