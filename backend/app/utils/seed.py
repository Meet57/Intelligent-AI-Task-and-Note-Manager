import random
from datetime import datetime, timedelta
from app.utils import db_utils

# Convenience aliases so existing seed code can call the same function names
create_note = db_utils.create_note
create_task = db_utils.create_task
add_note_to_task = db_utils.add_note_to_task

def seed_data():
    """Seed the database with realistic CS student tasks and notes."""
    
    # Create notes first
    notes = []
    
    notes.append(create_note(
        "Algorithm Complexity Review",
        "Focus on Big O notation: O(1), O(log n), O(n), O(n log n), O(n²). Practice identifying time complexity in recursive functions. Master theorem for divide-and-conquer algorithms.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Data Structures Cheat Sheet",
        "Arrays: O(1) access, O(n) insert. LinkedList: O(n) access, O(1) insert at head. HashMap: O(1) avg lookup. BST: O(log n) balanced operations. Use ArrayList for random access, LinkedList for frequent insertions.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "SQL JOIN Types",
        "INNER JOIN: matching rows only. LEFT JOIN: all from left + matches from right. RIGHT JOIN: opposite. FULL OUTER JOIN: all rows from both. Remember to use ON for join conditions.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Design Patterns",
        "Singleton: one instance globally. Factory: create objects without specifying class. Observer: publish-subscribe model. Strategy: encapsulate algorithms. Decorator: add functionality dynamically.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Git Commands",
        "git checkout -b: create new branch. git rebase: reapply commits. git cherry-pick: apply specific commit. git stash: save uncommitted changes. git reset --hard: discard all changes. Always pull before push.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "REST API Best Practices",
        "Use HTTP methods correctly: GET (read), POST (create), PUT (update), DELETE (remove). Return proper status codes: 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error. Use JSON format.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Python Tips",
        "Use list comprehensions for cleaner code. Remember self in instance methods. Use *args and **kwargs for flexible functions. Virtual environments isolate dependencies. PEP 8 style guide for formatting.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Network Protocols",
        "TCP: reliable, connection-oriented, slower. UDP: unreliable, connectionless, faster. HTTP runs on TCP port 80. HTTPS on 443. DNS uses UDP port 53. Three-way handshake: SYN, SYN-ACK, ACK.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Database Normalization",
        "1NF: atomic values, no repeating groups. 2NF: 1NF + no partial dependencies. 3NF: 2NF + no transitive dependencies. Denormalize for performance when needed. Foreign keys maintain referential integrity.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Testing Strategies",
        "Unit tests: test individual functions. Integration tests: test component interactions. E2E tests: test full user flows. Aim for 80% code coverage. Use mocks for external dependencies. TDD: write tests first.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "React Hooks",
        "useState: manage component state. useEffect: side effects and lifecycle. useContext: access context values. useMemo: memoize expensive calculations. useCallback: memoize functions. Custom hooks for reusable logic.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Security Considerations",
        "Always hash passwords with bcrypt or Argon2. Use prepared statements to prevent SQL injection. Implement CSRF tokens. Enable CORS carefully. Validate all user inputs. Keep dependencies updated for security patches.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "OS Process Scheduling",
        "FCFS: first come first served, simple but causes convoy effect. SJF: shortest job first, optimal but starvation possible. Round Robin: fair time slicing. Priority scheduling: use aging to prevent starvation.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Binary Search Implementation",
        "Always use left + (right - left) // 2 to avoid overflow. Remember the loop condition: while left <= right. Update bounds: left = mid + 1 or right = mid - 1. Time complexity O(log n).",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Docker Commands",
        "docker build -t name:tag . to build image. docker run -d -p 8080:80 to run detached. docker-compose up for multi-container. docker exec -it container bash for shell access. Use .dockerignore to exclude files.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "CSS Flexbox",
        "display: flex on container. justify-content: aligns main axis (horizontal). align-items: aligns cross axis (vertical). flex-direction: row or column. flex-wrap: wrap for responsive. gap: spacing between items.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Recursion Tips",
        "Always define base case first to prevent infinite recursion. Recursive case should move towards base case. Stack overflow risk with deep recursion. Consider iterative solution or tail recursion optimization.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Graph Algorithms",
        "BFS: shortest path in unweighted graph, use queue. DFS: detect cycles, use stack or recursion. Dijkstra: shortest path with weights, use priority queue. Bellman-Ford: handles negative weights.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Machine Learning Basics",
        "Supervised: labeled data (classification, regression). Unsupervised: unlabeled data (clustering, dimensionality reduction). Train/test split: 80/20 or 70/30. Overfitting: model too complex, use regularization.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Linux Commands",
        "grep: search text patterns. awk: text processing. sed: stream editor for substitution. chmod: change file permissions. ps aux: list processes. tail -f: follow log files in real-time.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Memory Management",
        "Stack: automatic, LIFO, fixed size, fast. Heap: manual/GC, dynamic size, slower, fragmentation possible. Memory leak: allocated but not freed. Use valgrind to detect leaks in C/C++.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Agile Methodology",
        "Sprints: 1-4 week iterations. Daily standups: 15 min sync. Sprint planning: estimate story points. Retrospective: reflect and improve. User stories: As a [role], I want [feature], so that [benefit].",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "JavaScript Promises",
        "Promise states: pending, fulfilled, rejected. .then() for success, .catch() for errors. Promise.all() waits for all, fails if any fails. Promise.race() resolves with first. async/await is syntactic sugar.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Sorting Algorithms",
        "Bubble Sort: O(n²), simple, stable. Quick Sort: O(n log n) avg, unstable, in-place. Merge Sort: O(n log n), stable, needs extra space. Heap Sort: O(n log n), unstable, in-place. Use built-in sort usually.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "CAP Theorem",
        "Consistency: all nodes see same data. Availability: every request gets response. Partition Tolerance: system works despite network splits. Can only guarantee 2 of 3. NoSQL often chooses AP or CP over CA.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "Regex Patterns",
        "\\d: digit, \\w: word char, \\s: whitespace. +: one or more, *: zero or more, ?: zero or one. []: character class, ^: start, $: end. (): capture group. Use raw strings r'' in Python.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "CI/CD Pipeline",
        "Continuous Integration: automated builds and tests on commit. Continuous Deployment: auto deploy to production. Use GitHub Actions, Jenkins, or GitLab CI. Run linters, tests, security scans before deploy.",
        datetime.now().isoformat()
    ))
    
    notes.append(create_note(
        "API Authentication",
        "JWT: stateless tokens with signature. OAuth2: delegated authorization. API Keys: simple but less secure. Session cookies: stateful, server-side storage. Always use HTTPS. Implement rate limiting.",
        datetime.now().isoformat()
    ))
    
    # Create tasks and associate notes
    today = datetime.now()
    
    # Task 1
    task1 = create_task(
        "Complete Data Structures Assignment 3",
        "Implement AVL tree with insertion, deletion, and balancing. Include test cases and time complexity analysis.",
        "pending",
        (today + timedelta(days=3)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task1, notes[1])
    add_note_to_task(task1, notes[0])
    
    # Task 2
    task2 = create_task(
        "Study for Algorithms Midterm",
        "Review sorting algorithms, graph traversal, dynamic programming, and greedy algorithms. Practice problems from chapters 4-7.",
        "in_progress",
        (today + timedelta(days=5)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task2, notes[0])
    
    # Task 3
    task3 = create_task(
        "Database Project: E-commerce Schema",
        "Design normalized database schema for online store. Include users, products, orders, and reviews tables. Write SQL queries for common operations.",
        "in_progress",
        (today + timedelta(days=7)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task3, notes[2])
    add_note_to_task(task3, notes[8])
    
    # Task 4
    task4 = create_task(
        "Software Engineering: Implement Design Patterns",
        "Refactor existing codebase to use Factory and Observer patterns. Document design decisions and UML diagrams.",
        "pending",
        (today + timedelta(days=10)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task4, notes[3])
    
    # Task 5
    task5 = create_task(
        "Web Dev: Build REST API for Todo App",
        "Create Express.js backend with CRUD endpoints. Implement authentication with JWT. Write API documentation.",
        "pending",
        (today + timedelta(days=6)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task5, notes[5])
    add_note_to_task(task5, notes[11])
    
    # Task 6
    task6 = create_task(
        "Contribute to Open Source Project",
        "Fix issue #234 in react-testing-library repo. Set up development environment and submit PR with tests.",
        "pending",
        (today + timedelta(days=14)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task6, notes[4])
    add_note_to_task(task6, notes[9])
    
    # Task 7
    task7 = create_task(
        "Computer Networks Lab: Socket Programming",
        "Implement chat application using TCP sockets. Support multiple clients and message broadcasting.",
        "in_progress",
        (today + timedelta(days=4)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task7, notes[7])
    add_note_to_task(task7, notes[6])
    
    # Task 8
    task8 = create_task(
        "Write Unit Tests for Calculator Module",
        "Achieve 90% code coverage for calculator.py. Test edge cases including division by zero and floating point precision.",
        "completed",
        (today - timedelta(days=2)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task8, notes[9])
    add_note_to_task(task8, notes[6])
    
    # Task 9
    task9 = create_task(
        "Frontend: Rebuild Dashboard with React Hooks",
        "Migrate class components to functional components. Optimize re-renders with useMemo and useCallback.",
        "pending",
        (today + timedelta(days=12)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task9, notes[10])
    
    # Task 10
    task10 = create_task(
        "Security Audit: Fix Vulnerabilities in Project",
        "Address SQL injection risks, implement input validation, update deprecated dependencies. Run OWASP ZAP scan.",
        "pending",
        (today + timedelta(days=8)).strftime("%Y-%m-%d")
    )
    add_note_to_task(task10, notes[11])
    add_note_to_task(task10, notes[2])
    
    print("✅ Database seeded successfully!")
    print(f"Created {len(notes)} notes and 10 tasks with associations")
    print("\nNote topics included:")
    print("- Algorithms & Data Structures")
    print("- Databases & SQL")
    print("- Web Development")
    print("- System Design & Architecture")
    print("- DevOps & Tools")
    print("- Programming Languages")
    print("- Software Engineering Practices")


if __name__ == "__main__":
    from app.db import init_db
    init_db()
    seed_data()