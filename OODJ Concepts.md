# OODJ Concepts in Academic Feedback System (AFS)

This document outlines the Object-Oriented Design in Java (OODJ) concepts implemented in your project, with specific code examples.

## 1. Encapsulation

Encapsulation is the process of wrapping data (variables) and code acting on the data (methods) together as a single unit. In OODJ, this is achieved by making fields `private` and providing `public` getters and setters.

**Example: [Module.java](file:///c:/Users/dinee/Downloads/APU/JAVA/Java%20Ass%20Versions/Java%20Ass/src/afs/models/Module.java)**

```java
public class Module {
    // Private fields - Hidden from outside classes
    private String moduleCode;
    private String moduleName;

    // Public Getters and Setters - Controlled access
    public String getModuleCode() {
        return moduleCode;
    }

    public void setModuleCode(String moduleCode) {
        this.moduleCode = moduleCode;
    }
}
```

> [!NOTE]
> This prevents external classes from accidentally modifying data without validation.

---

## 2. Inheritance

Inheritance allows a class (subclass) to acquire the properties and behaviors of another class (superclass). This promotes code reusability.

**Example: [Lecturer.java](file:///c:/Users/dinee/Downloads/APU/JAVA/Java%20Ass%20Versions/Java%20Ass/src/afs/models/Lecturer.java)**

```java
// Lecturer "is-a" User
public class Lecturer extends User {
    public Lecturer(String id, String username, ...) {
        // Calls the constructor of the parent class (User)
        super(id, username, ...);
    }
}
```

> [!TIP]
> By extending `User`, the `Lecturer` class automatically gets fields like `id`, `name`, and `email` without rewriting them.

---

## 3. Abstraction

Abstraction focuses on hiding the complex implementation details and showing only the necessary features of an object. It is implemented using `abstract` classes and methods.

**Example: [User.java](file:///c:/Users/dinee/Downloads/APU/JAVA/Java%20Ass%20Versions/Java%20Ass/src/afs/models/User.java)**

```java
public abstract class User {
    // Abstract method: No body, must be implemented by subclasses
    public abstract String[] getMenuOptions();
}
```

> [!IMPORTANT]
> Because `User` is `abstract`, you cannot do `new User()`. You must create a specific type like `new Student()`.

---

## 4. Polymorphism

Polymorphism allows one interface to be used for a general class of actions. The most common form is **Method Overriding**, where a subclass provides a specific implementation of a method already defined in its parent.

**Example: [Lecturer.java](file:///c:/Users/dinee/Downloads/APU/JAVA/Java%20Ass%20Versions/Java%20Ass/src/afs/models/Lecturer.java)**

```java
@Override
public String[] getMenuOptions() {
    // Specific menu for Lecturers
    return new String[] { "Manage Assessments", "Enter Marks", ... };
}
```

In **[DashboardPanel.java](file:///c:/Users/dinee/Downloads/APU/JAVA/Java%20Ass%20Versions/Java%20Ass/src/afs/ui/DashboardPanel.java)**:

```java
// This single line works for Students, Lecturers, and Admins!
// The JVM decides which getMenuOptions() to call at runtime.
String[] menuOptions = user.getMenuOptions();
```

---

## 5. Singleton Design Pattern

The Singleton pattern ensures a class has only one instance and provides a global point of access to it.

**Example: [DataManager.java](file:///c:/Users/dinee/Downloads/APU/JAVA/Java%20Ass%20Versions/Java%20Ass/src/afs/utils/DataManager.java)**

```java
public class DataManager {
    private static DataManager instance;

    // Private constructor prevents creation of new instances via 'new'
    private DataManager() { ... }

    // Global access point
    public static DataManager getInstance() {
        if (instance == null) {
            instance = new DataManager();
        }
        return instance;
    }
}
```

---

## 6. Modularity

Modularity is the design principle of subdividing a system into smaller parts called modules, which can be independently created, modified, replaced, or exchanged. In Java, this is primarily achieved through **Packages**.

### Key Implementation: Package Structure

Your project is highly modular, separating code into distinctive layers:

1. **`afs.models` Package**:
    * **Responsibility**: Defines the data structure (User, Student, Grade).
    * **Benefit**: If you need to change how a Student is stored (e.g., add a new field), you only touch this package. The UI code doesn't need to know the details.

2. **`afs.ui` Package**:
    * **Responsibility**: Handles all graphical interfaces (`LoginPanel`, `DashboardPanel`).
    * **Benefit**: You can completely redesign the look of the app (like we did with `UITheme`) without breaking the business logic or data saving mechanisms.

3. **`afs.utils` Package**:
    * **Responsibility**: Helper classes for global operations (`DataManager`, `AuthManager`).
    * **Benefit**: File I/O logic is centralized. If you switch from text files to a database later, you only modify `DataManager`. The rest of the app remains untouched.

**Example Directory Structure:**

```text
src/afs/
├── models/       <-- Data Layer
│   ├── User.java
│   └── Student.java
├── ui/           <-- Presentation Layer
│   ├── LoginPanel.java
│   └── DashboardPanel.java
└── utils/        <-- Logic/Service Layer
    ├── DataManager.java
    └── AuthManager.java
```
