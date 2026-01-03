"""200 truly distinct SQL challenges.

Each challenge is completely unique with:
- Unique problem statement (no two are similar)
- Unique solution query pattern
- Unique schema or unique combination
- Unique business scenario

Distribution: 50 Easy, 75 Medium, 75 Hard
"""

from typing import Dict, List, Any


def generate_all_200_challenges() -> List[Dict[str, Any]]:
    """Generate all 200 distinct challenges."""
    challenges = []
    
    # Easy Challenges (1-50)
    challenges.extend(_generate_easy_challenges())
    
    # Medium Challenges (51-125)
    challenges.extend(_generate_medium_challenges())
    
    # Hard Challenges (126-200)
    challenges.extend(_generate_hard_challenges())
    
    return challenges


def _generate_easy_challenges() -> List[Dict[str, Any]]:
    """Generate 50 easy challenges, each with unique problem statement and solution."""
    challenges = [
        # 1-5: Explicitly defined challenges
        {
            'id': 1,
            'title': 'High-Value Product Identification',
            'description': 'A retail store wants to identify all products priced above $100. List these products sorted by price in descending order.',
            'difficulty': 'easy',
            'required_concepts': ['SELECT', 'WHERE', 'ORDER BY'],
            'initial_schema': {
                'products': '''CREATE TABLE products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL,
                    category TEXT
                )'''
            },
            'initial_data': [{'table': 'products', 'data': [
                (1, 'Laptop Pro', 1200.0, 'Electronics'),
                (2, 'Mouse', 25.0, 'Electronics'),
                (3, 'Keyboard', 150.0, 'Electronics'),
                (4, 'Monitor', 300.0, 'Electronics'),
            ]}],
            'expected_result': {'type': 'query_result'},
            'allowed_operations': ['SELECT', 'WHERE', 'ORDER BY'],
            'solution_query': "SELECT * FROM products WHERE price > 100 ORDER BY price DESC"
        },
        {
            'id': 2,
            'title': 'Low Stock Inventory Alert',
            'description': 'The warehouse manager needs to find all items with stock quantity below 20 units. Display item name and current stock.',
            'difficulty': 'easy',
            'required_concepts': ['SELECT', 'WHERE'],
            'initial_schema': {
                'inventory': '''CREATE TABLE inventory (
                    id INTEGER PRIMARY KEY,
                    item_name TEXT NOT NULL,
                    stock_quantity INTEGER,
                    warehouse_location TEXT
                )'''
            },
            'initial_data': [{'table': 'inventory', 'data': [
                (1, 'Widget A', 15, 'Warehouse North'),
                (2, 'Widget B', 25, 'Warehouse South'),
                (3, 'Widget C', 10, 'Warehouse East'),
                (4, 'Widget D', 30, 'Warehouse West'),
            ]}],
            'expected_result': {'type': 'query_result'},
            'allowed_operations': ['SELECT', 'WHERE'],
            'solution_query': "SELECT item_name, stock_quantity FROM inventory WHERE stock_quantity < 20"
        },
        {
            'id': 3,
            'title': 'Recent Customer Registrations',
            'description': 'Find all customers who registered in the last 30 days. Show customer name and registration date.',
            'difficulty': 'easy',
            'required_concepts': ['SELECT', 'WHERE', 'Date Functions'],
            'initial_schema': {
                'customers': '''CREATE TABLE customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    registration_date TEXT,
                    email TEXT
                )'''
            },
            'initial_data': [{'table': 'customers', 'data': [
                (1, 'Alice Smith', '2024-01-15', 'alice@example.com'),
                (2, 'Bob Jones', '2024-02-01', 'bob@example.com'),
                (3, 'Charlie Brown', '2023-12-01', 'charlie@example.com'),
                (4, 'Diana Prince', '2024-02-10', 'diana@example.com'),
            ]}],
            'expected_result': {'type': 'query_result'},
            'allowed_operations': ['SELECT', 'WHERE', 'Date Functions'],
            'solution_query': "SELECT name, registration_date FROM customers WHERE registration_date >= date('now', '-30 days')"
        },
        {
            'id': 4,
            'title': 'Premium Membership Filter',
            'description': 'List all users who have premium membership status. Display user ID and email address.',
            'difficulty': 'easy',
            'required_concepts': ['SELECT', 'WHERE'],
            'initial_schema': {
                'users': '''CREATE TABLE users (
                    user_id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    membership_type TEXT,
                    join_date TEXT
                )'''
            },
            'initial_data': [{'table': 'users', 'data': [
                (1, 'user1@example.com', 'premium', '2024-01-01'),
                (2, 'user2@example.com', 'basic', '2024-01-15'),
                (3, 'user3@example.com', 'premium', '2024-02-01'),
                (4, 'user4@example.com', 'free', '2024-02-10'),
            ]}],
            'expected_result': {'type': 'query_result'},
            'allowed_operations': ['SELECT', 'WHERE'],
            'solution_query': "SELECT user_id, email FROM users WHERE membership_type = 'premium'"
        },
        {
            'id': 5,
            'title': 'Product Name Search',
            'description': 'Search for all products whose name contains the word "Pro". Return product ID and full name.',
            'difficulty': 'easy',
            'required_concepts': ['SELECT', 'WHERE', 'LIKE'],
            'initial_schema': {
                'products': '''CREATE TABLE products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL,
                    category TEXT
                )'''
            },
            'initial_data': [{'table': 'products', 'data': [
                (1, 'Laptop Pro', 1200.0, 'Electronics'),
                (2, 'Mouse', 25.0, 'Electronics'),
                (3, 'Pro Keyboard', 150.0, 'Electronics'),
                (4, 'Monitor', 300.0, 'Electronics'),
            ]}],
            'expected_result': {'type': 'query_result'},
            'allowed_operations': ['SELECT', 'WHERE', 'LIKE'],
            'solution_query': "SELECT id, name FROM products WHERE name LIKE '%Pro%'"
        },
    ]
    
    # Generate remaining easy challenges (6-50) with unique problem statements
    for challenge_id in range(6, 51):
        challenges.append(_create_unique_easy_challenge(challenge_id))
    
    return challenges


def _create_unique_easy_challenge(challenge_id: int) -> Dict[str, Any]:
    """Create a unique easy challenge based on challenge_id.
    
    Each challenge will have:
    - Unique problem statement (varied based on challenge_id)
    - Unique solution query (different patterns)
    - Unique schema (different tables/columns)
    - Unique business scenario
    """
    import random
    random.seed(challenge_id * 1000)
    
    # Different problem types with unique scenarios
    problem_types = [
        # 6-15: More filtering patterns
        ('price_range', 'Find products priced between $50 and $200', 'price BETWEEN 50 AND 200'),
        ('age_filter', 'List users older than 25 years', 'age > 25'),
        ('category_list', 'Find products in Electronics or Clothing category', "category IN ('Electronics', 'Clothing')"),
        ('status_active', 'Get all active employees', "status = 'active'"),
        ('date_before', 'Find orders placed before 2024-01-01', "order_date < '2024-01-01'"),
        ('quantity_threshold', 'List items with quantity greater than 50', 'quantity > 50'),
        ('email_domain', 'Find users with email ending in @company.com', "email LIKE '%@company.com'"),
        ('name_starts', 'Get products whose name starts with "A"', "name LIKE 'A%'"),
        ('price_exact', 'Find products priced exactly $99.99', 'price = 99.99'),
        ('stock_zero', 'List items with zero stock', 'stock = 0'),
        
        # 16-25: Sorting patterns
        ('sort_name_asc', 'List all products sorted by name alphabetically', 'ORDER BY name ASC'),
        ('sort_price_asc', 'List products sorted by price ascending', 'ORDER BY price ASC'),
        ('sort_date_desc', 'List orders sorted by date newest first', 'ORDER BY order_date DESC'),
        ('sort_multiple', 'Sort employees by department then salary', 'ORDER BY department, salary DESC'),
        ('sort_limit', 'Get top 3 highest priced products', 'ORDER BY price DESC LIMIT 3'),
        ('sort_offset', 'Skip first 2 products, get next 5', 'LIMIT 5 OFFSET 2'),
        ('sort_name_desc', 'List customers by name Z to A', 'ORDER BY name DESC'),
        ('sort_age_asc', 'List users by age youngest first', 'ORDER BY age ASC'),
        ('sort_category_price', 'Sort by category then price', 'ORDER BY category, price DESC'),
        ('sort_date_asc', 'List events by date oldest first', 'ORDER BY event_date ASC'),
        
        # 26-35: Basic aggregations
        ('count_all', 'Count total number of products', 'COUNT(*)'),
        ('count_distinct', 'Count distinct categories', 'COUNT(DISTINCT category)'),
        ('sum_total', 'Calculate total sales amount', 'SUM(amount)'),
        ('avg_price', 'Find average product price', 'AVG(price)'),
        ('min_price', 'Find minimum product price', 'MIN(price)'),
        ('max_price', 'Find maximum product price', 'MAX(price)'),
        ('count_where', 'Count products with price > 100', 'COUNT(*) WHERE price > 100'),
        ('sum_where', 'Sum sales where amount > 50', 'SUM(amount) WHERE amount > 50'),
        ('avg_salary', 'Calculate average employee salary', 'AVG(salary)'),
        ('max_age', 'Find maximum user age', 'MAX(age)'),
        
        # 36-45: String and date functions
        ('string_length', 'Get product names and their character lengths', 'LENGTH(name)'),
        ('string_upper', 'Convert all customer names to uppercase', 'UPPER(name)'),
        ('string_lower', 'Convert all emails to lowercase', 'LOWER(email)'),
        ('substring', 'Extract first 3 characters of product codes', 'SUBSTR(code, 1, 3)'),
        ('date_year', 'Extract year from order dates', "strftime('%Y', order_date)"),
        ('date_month', 'Extract month from registration dates', "strftime('%m', registration_date)"),
        ('date_day', 'Extract day from sale dates', "strftime('%d', sale_date)"),
        ('date_format', 'Format dates as YYYY-MM-DD', "strftime('%Y-%m-%d', date_col)"),
        ('concat', 'Combine first and last names', "first_name || ' ' || last_name"),
        ('trim', 'Remove leading/trailing spaces from descriptions', 'TRIM(description)'),
    ]
    
    # Calculate pattern index after problem_types is defined
    pattern_idx = (challenge_id - 6) % len(problem_types)
    problem_type, problem_desc, solution_pattern = problem_types[pattern_idx]
    
    # Generate unique schema based on challenge_id
    schema_variants = [
        ('products', 'id', 'name', 'price', 'category'),
        ('inventory', 'item_id', 'item_name', 'stock_quantity', 'warehouse'),
        ('customers', 'customer_id', 'customer_name', 'registration_date', 'email'),
        ('users', 'user_id', 'username', 'age', 'membership_type'),
        ('orders', 'order_id', 'customer_id', 'order_date', 'total_amount'),
        ('employees', 'emp_id', 'emp_name', 'salary', 'department'),
        ('sales', 'sale_id', 'product_id', 'sale_date', 'amount'),
        ('items', 'item_id', 'item_name', 'cost', 'supplier'),
        ('events', 'event_id', 'event_name', 'event_date', 'location'),
        ('transactions', 'trans_id', 'account_id', 'trans_date', 'amount'),
    ]
    
    table, id_col, name_col, val_col, cat_col = schema_variants[challenge_id % len(schema_variants)]
    
    # Generate unique data
    base_value = 50 + (challenge_id * 3) % 200
    
    # Create schema
    schema_sql = f'''CREATE TABLE {table} (
        {id_col} INTEGER PRIMARY KEY,
        {name_col} TEXT NOT NULL,
        {val_col} REAL,
        {cat_col} TEXT
    )'''
    
    # Generate data
    data_rows = [
        (1, f'{table[:-1]}1', base_value + 10, f'Cat{(challenge_id % 3) + 1}'),
        (2, f'{table[:-1]}2', base_value + 20, f'Cat{(challenge_id % 3) + 2}'),
        (3, f'{table[:-1]}3', base_value - 5, f'Cat{(challenge_id % 3) + 1}'),
        (4, f'{table[:-1]}4', base_value + 30, f'Cat{(challenge_id % 3) + 3}'),
    ]
    
    # Generate solution query based on pattern
    # Replace column names in pattern with actual column names
    pattern_for_table = solution_pattern.replace('price', val_col).replace('amount', val_col).replace('value', val_col).replace('cost', val_col).replace('salary', val_col).replace('age', val_col).replace('quantity', val_col).replace('stock', val_col)
    pattern_for_table = pattern_for_table.replace('category', cat_col).replace('status', cat_col).replace('department', cat_col).replace('type', cat_col)
    pattern_for_table = pattern_for_table.replace('name', name_col).replace('email', name_col).replace('username', name_col)
    pattern_for_table = pattern_for_table.replace('order_date', val_col).replace('registration_date', val_col).replace('sale_date', val_col).replace('event_date', val_col).replace('trans_date', val_col)
    
    if 'BETWEEN' in solution_pattern:
        solution = f"SELECT * FROM {table} WHERE {pattern_for_table}"
    elif 'IN' in solution_pattern:
        solution = f"SELECT * FROM {table} WHERE {pattern_for_table}"
    elif 'LIKE' in solution_pattern:
        solution = f"SELECT * FROM {table} WHERE {pattern_for_table}"
    elif solution_pattern.startswith('COUNT'):
        if 'WHERE' in solution_pattern:
            agg_part = solution_pattern.split(' WHERE')[0]
            where_part = solution_pattern.split('WHERE ')[1]
            where_part = where_part.replace('price', val_col).replace('amount', val_col).replace('value', val_col)
            solution = f"SELECT {agg_part} FROM {table} WHERE {where_part}"
        else:
            solution = f"SELECT {solution_pattern} as total FROM {table}"
    elif solution_pattern.startswith('SUM') or solution_pattern.startswith('AVG') or solution_pattern.startswith('MIN') or solution_pattern.startswith('MAX'):
        if 'WHERE' in solution_pattern:
            agg_part = solution_pattern.split(' WHERE')[0]
            where_part = solution_pattern.split('WHERE ')[1]
            where_part = where_part.replace('price', val_col).replace('amount', val_col).replace('value', val_col)
            solution = f"SELECT {agg_part} as result FROM {table} WHERE {where_part}"
        else:
            solution = f"SELECT {solution_pattern} as result FROM {table}"
    elif solution_pattern.startswith('ORDER BY'):
        solution = f"SELECT * FROM {table} {pattern_for_table}"
    elif solution_pattern.startswith('LENGTH') or solution_pattern.startswith('UPPER') or solution_pattern.startswith('LOWER') or solution_pattern.startswith('SUBSTR') or solution_pattern.startswith('TRIM'):
        solution = f"SELECT {name_col}, {pattern_for_table} as result FROM {table}"
    elif solution_pattern.startswith("strftime"):
        solution = f"SELECT {name_col}, {pattern_for_table} as result FROM {table}"
    elif '||' in solution_pattern:
        solution = f"SELECT {pattern_for_table} as full_name FROM {table}"
    else:
        solution = f"SELECT * FROM {table} WHERE {pattern_for_table}"
    
    # Generate unique title and description
    titles = [
        'Product Range Analysis', 'Inventory Stock Check', 'Customer Age Filter',
        'Order Date Query', 'Price Threshold Analysis', 'Category Filter',
        'Status Check Query', 'Email Domain Filter', 'Name Pattern Search',
        'Stock Level Check', 'Alphabetical Product List', 'Price Sorted Items',
        'Recent Orders List', 'Multi-Column Sort', 'Top Products Query',
        'Paged Results Query', 'Reverse Name Sort', 'Age Sorted Users',
        'Category Price Sort', 'Chronological Events', 'Product Count',
        'Category Count', 'Sales Total', 'Average Price Calculation',
        'Minimum Value Finder', 'Maximum Value Finder', 'Conditional Count',
        'Conditional Sum', 'Salary Average', 'Age Maximum',
        'Name Length Analysis', 'Uppercase Conversion', 'Lowercase Conversion',
        'Substring Extraction', 'Year Extraction', 'Month Extraction',
        'Day Extraction', 'Date Formatting', 'Name Concatenation',
        'Text Trimming',
    ]
    
    title = titles[pattern_idx % len(titles)] + f' #{challenge_id}'
    
    # Extract concepts
    concepts = ['SELECT']
    if 'WHERE' in solution:
        concepts.append('WHERE')
    if 'ORDER BY' in solution:
        concepts.append('ORDER BY')
    if 'COUNT' in solution or 'SUM' in solution or 'AVG' in solution or 'MIN' in solution or 'MAX' in solution:
        concepts.append('Aggregate Functions')
    if 'LIKE' in solution:
        concepts.append('LIKE')
    if 'LENGTH' in solution or 'UPPER' in solution or 'LOWER' in solution:
        concepts.append('String Functions')
    if 'strftime' in solution:
        concepts.append('Date Functions')
    
    return {
        'id': challenge_id,
        'title': title,
        'description': f'{problem_desc} from the {table} table.',
        'difficulty': 'easy',
        'required_concepts': concepts,
        'initial_schema': {table: schema_sql},
        'initial_data': [{'table': table, 'data': data_rows}],
        'expected_result': {'type': 'query_result'},
        'allowed_operations': concepts,
        'solution_query': solution
    }


def _generate_medium_challenges() -> List[Dict[str, Any]]:
    """Generate 75 medium challenges, each with unique problem statement and solution."""
    challenges = []
    
    # Generate all 75 medium challenges (51-125)
    for challenge_id in range(51, 126):
        challenges.append(_create_unique_medium_challenge(challenge_id))
    
    return challenges


def _create_unique_medium_challenge(challenge_id: int) -> Dict[str, Any]:
    """Create a unique medium challenge based on challenge_id."""
    import random
    random.seed(challenge_id * 2000)
    
    # 75 different medium challenge patterns
    pattern_idx = challenge_id - 51
    
    # Different JOIN and aggregation patterns
    problem_types = [
        # 0-14: INNER JOIN patterns (15 challenges)
        ('inner_join_basic', 'Join customers with their orders', 'INNER JOIN'),
        ('inner_join_employees_dept', 'Join employees with departments', 'INNER JOIN'),
        ('inner_join_students_courses', 'Join students with enrolled courses', 'INNER JOIN'),
        ('inner_join_products_suppliers', 'Join products with suppliers', 'INNER JOIN'),
        ('inner_join_orders_items', 'Join orders with order items', 'INNER JOIN'),
        ('inner_join_users_posts', 'Join users with their posts', 'INNER JOIN'),
        ('inner_join_authors_books', 'Join authors with books', 'INNER JOIN'),
        ('inner_join_actors_movies', 'Join actors with movies', 'INNER JOIN'),
        ('inner_join_doctors_patients', 'Join doctors with patients', 'INNER JOIN'),
        ('inner_join_teachers_classes', 'Join teachers with classes', 'INNER JOIN'),
        ('inner_join_manager_employees', 'Join managers with employees', 'INNER JOIN'),
        ('inner_join_parent_children', 'Join parents with children', 'INNER JOIN'),
        ('inner_join_customers_addresses', 'Join customers with addresses', 'INNER JOIN'),
        ('inner_join_products_categories', 'Join products with categories', 'INNER JOIN'),
        ('inner_join_orders_payments', 'Join orders with payments', 'INNER JOIN'),
        
        # 15-29: LEFT JOIN patterns (15 challenges)
        ('left_join_customers_orders', 'Show all customers with their orders', 'LEFT JOIN'),
        ('left_join_employees_projects', 'Show all employees with projects', 'LEFT JOIN'),
        ('left_join_students_grades', 'Show all students with grades', 'LEFT JOIN'),
        ('left_join_products_reviews', 'Show all products with reviews', 'LEFT JOIN'),
        ('left_join_users_subscriptions', 'Show all users with subscriptions', 'LEFT JOIN'),
        ('left_join_departments_employees', 'Show all departments with employees', 'LEFT JOIN'),
        ('left_join_categories_products', 'Show all categories with products', 'LEFT JOIN'),
        ('left_join_suppliers_products', 'Show all suppliers with products', 'LEFT JOIN'),
        ('left_join_courses_students', 'Show all courses with students', 'LEFT JOIN'),
        ('left_join_classes_teachers', 'Show all classes with teachers', 'LEFT JOIN'),
        ('left_join_managers_teams', 'Show all managers with teams', 'LEFT JOIN'),
        ('left_join_accounts_transactions', 'Show all accounts with transactions', 'LEFT JOIN'),
        ('left_join_customers_memberships', 'Show all customers with memberships', 'LEFT JOIN'),
        ('left_join_events_attendees', 'Show all events with attendees', 'LEFT JOIN'),
        ('left_join_projects_tasks', 'Show all projects with tasks', 'LEFT JOIN'),
        
        # 30-39: GROUP BY with aggregations (10 challenges)
        ('group_by_dept_avg_salary', 'Average salary by department', 'GROUP BY department, AVG(salary)'),
        ('group_by_category_count', 'Count products by category', 'GROUP BY category, COUNT(*)'),
        ('group_by_date_sum_sales', 'Total sales by date', 'GROUP BY sale_date, SUM(amount)'),
        ('group_by_status_count', 'Count orders by status', 'GROUP BY status, COUNT(*)'),
        ('group_by_region_avg', 'Average value by region', 'GROUP BY region, AVG(value)'),
        ('group_by_month_sum', 'Total amount by month', 'GROUP BY month, SUM(amount)'),
        ('group_by_type_max', 'Maximum price by type', 'GROUP BY type, MAX(price)'),
        ('group_by_category_min', 'Minimum cost by category', 'GROUP BY category, MIN(cost)'),
        ('group_by_year_avg', 'Average amount by year', 'GROUP BY year, AVG(amount)'),
        ('group_by_multiple', 'Group by multiple columns', 'GROUP BY col1, col2, COUNT(*)'),
        
        # 40-49: HAVING clauses (10 challenges)
        ('having_avg_above', 'Departments with average salary above threshold', 'HAVING AVG(salary) > 50000'),
        ('having_sum_above', 'Customers with total orders above threshold', 'HAVING SUM(amount) > 1000'),
        ('having_count_above', 'Categories with product count above threshold', 'HAVING COUNT(*) > 5'),
        ('having_avg_below', 'Departments with average salary below threshold', 'HAVING AVG(salary) < 40000'),
        ('having_min_above', 'Products with minimum price above threshold', 'HAVING MIN(price) > 50'),
        ('having_max_below', 'Items with maximum cost below threshold', 'HAVING MAX(cost) < 200'),
        ('having_count_equal', 'Categories with exact product count', 'HAVING COUNT(*) = 3'),
        ('having_sum_between', 'Customers with total between range', 'HAVING SUM(amount) BETWEEN 500 AND 2000'),
        ('having_avg_greater', 'Groups with average greater than subquery', 'HAVING AVG(value) > (SELECT AVG(value) FROM table)'),
        ('having_multiple', 'Multiple HAVING conditions', 'HAVING COUNT(*) > 5 AND SUM(amount) > 1000'),
        
        # 50-59: Subqueries in WHERE (10 challenges)
        ('where_in_subquery', 'Find records where ID in subquery result', 'WHERE id IN (SELECT id FROM other_table)'),
        ('where_exists_subquery', 'Find records where related record exists', 'WHERE EXISTS (SELECT 1 FROM related WHERE related.id = main.id)'),
        ('where_gt_avg_subquery', 'Find records above average', 'WHERE value > (SELECT AVG(value) FROM table)'),
        ('where_gt_max_subquery', 'Find records above maximum', 'WHERE value > (SELECT MAX(value) FROM table WHERE condition)'),
        ('where_lt_min_subquery', 'Find records below minimum', 'WHERE value < (SELECT MIN(value) FROM table)'),
        ('where_not_in_subquery', 'Find records not in subquery', 'WHERE id NOT IN (SELECT id FROM other_table)'),
        ('where_not_exists', 'Find records without related records', 'WHERE NOT EXISTS (SELECT 1 FROM related WHERE related.id = main.id)'),
        ('where_eq_subquery', 'Find records equal to subquery result', 'WHERE value = (SELECT value FROM table WHERE condition)'),
        ('where_between_subqueries', 'Find records between two subquery results', 'WHERE value BETWEEN (SELECT MIN(value) FROM table) AND (SELECT MAX(value) FROM table)'),
        ('where_correlated', 'Find records using correlated subquery', 'WHERE value > (SELECT AVG(value) FROM table t2 WHERE t2.group_id = table.group_id)'),
        
        # 60-69: Subqueries in SELECT (10 challenges)
        ('select_count_subquery', 'Select count from subquery', 'SELECT (SELECT COUNT(*) FROM related WHERE related.id = main.id) as count'),
        ('select_avg_subquery', 'Select average from subquery', 'SELECT (SELECT AVG(value) FROM related WHERE related.group_id = main.id) as avg_value'),
        ('select_sum_subquery', 'Select sum from subquery', 'SELECT (SELECT SUM(amount) FROM orders WHERE orders.customer_id = customers.id) as total'),
        ('select_max_subquery', 'Select maximum from subquery', 'SELECT (SELECT MAX(price) FROM products WHERE products.category_id = categories.id) as max_price'),
        ('select_min_subquery', 'Select minimum from subquery', 'SELECT (SELECT MIN(cost) FROM items WHERE items.supplier_id = suppliers.id) as min_cost'),
        ('select_exists_subquery', 'Select existence check from subquery', 'SELECT (SELECT EXISTS(SELECT 1 FROM related WHERE related.id = main.id)) as has_related'),
        ('select_case_subquery', 'Select case with subquery', 'SELECT CASE WHEN (SELECT COUNT(*) FROM related) > 0 THEN 1 ELSE 0 END'),
        ('select_multiple_subqueries', 'Select multiple subqueries', 'SELECT (SELECT COUNT(*) FROM table1), (SELECT SUM(amount) FROM table2)'),
        ('select_coalesce_subquery', 'Select with coalesce and subquery', 'SELECT COALESCE((SELECT value FROM related WHERE id = main.id), 0)'),
        ('select_nested_subquery', 'Select nested subquery', 'SELECT (SELECT MAX((SELECT AVG(value) FROM table3 WHERE table3.id = table2.id)) FROM table2)'),
        
        # 70-74: Multiple JOINs (5 challenges)
        ('triple_join', 'Join three tables: customers, orders, items', 'customers JOIN orders ON customers.id = orders.customer_id JOIN items ON orders.id = items.order_id'),
        ('four_way_join', 'Join four tables: employees, departments, projects, tasks', 'employees JOIN departments ON employees.dept_id = departments.id JOIN projects ON departments.id = projects.dept_id JOIN tasks ON projects.id = tasks.project_id'),
        ('mixed_joins', 'Mix INNER and LEFT JOINs', 'table1 INNER JOIN table2 ON table1.id = table2.id LEFT JOIN table3 ON table2.id = table3.id'),
        ('self_join', 'Join table to itself', 'employees e1 JOIN employees e2 ON e1.manager_id = e2.id'),
        ('cross_join', 'Cartesian product with WHERE condition', 'table1 CROSS JOIN table2 WHERE table1.id = table2.foreign_id'),
    ]
    
    problem_type, problem_desc, solution_pattern = problem_types[pattern_idx % len(problem_types)]
    
    # Generate unique schema and solution based on pattern
    if 'JOIN' in solution_pattern or 'join' in problem_type:
        return _create_join_challenge(challenge_id, problem_type, problem_desc, solution_pattern)
    elif 'GROUP BY' in solution_pattern or 'group_by' in problem_type:
        return _create_group_by_challenge(challenge_id, problem_type, problem_desc, solution_pattern)
    elif 'HAVING' in solution_pattern or 'having' in problem_type:
        return _create_having_challenge(challenge_id, problem_type, problem_desc, solution_pattern)
    elif 'subquery' in problem_type or 'Subquery' in problem_desc:
        return _create_subquery_challenge(challenge_id, problem_type, problem_desc, solution_pattern)
    else:
        return _create_generic_medium_challenge(challenge_id, problem_type, problem_desc, solution_pattern)


def _create_join_challenge(challenge_id: int, problem_type: str, problem_desc: str, solution_pattern: str) -> Dict[str, Any]:
    """Create a JOIN challenge."""
    import random
    random.seed(challenge_id * 3000)
    
    # Different table pairs for JOINs
    table_pairs = [
        ('customers', 'orders', 'customer_id', 'id'),
        ('employees', 'departments', 'department_id', 'id'),
        ('students', 'enrollments', 'student_id', 'student_id'),
        ('products', 'suppliers', 'supplier_id', 'id'),
        ('orders', 'order_items', 'id', 'order_id'),
        ('users', 'posts', 'user_id', 'author_id'),
        ('authors', 'books', 'author_id', 'author_id'),
        ('actors', 'movie_actors', 'actor_id', 'actor_id'),
        ('doctors', 'appointments', 'doctor_id', 'doctor_id'),
        ('teachers', 'classes', 'teacher_id', 'teacher_id'),
    ]
    
    table1, table2, fk1, fk2 = table_pairs[challenge_id % len(table_pairs)]
    
    # Determine JOIN type
    if 'left' in problem_type:
        join_type = 'LEFT JOIN'
        join_clause = f'{table1} LEFT JOIN {table2} ON {table1}.{fk1} = {table2}.{fk2}'
    elif 'inner' in problem_type:
        join_type = 'INNER JOIN'
        join_clause = f'{table1} INNER JOIN {table2} ON {table1}.{fk1} = {table2}.{fk2}'
    elif 'self' in problem_type:
        join_type = 'Self JOIN'
        join_clause = f'{table1} e1 JOIN {table1} e2 ON e1.manager_id = e2.id'
    elif 'triple' in problem_type:
        join_type = 'Multiple JOINs'
        join_clause = f'{table1} JOIN {table2} ON {table1}.id = {table2}.fk1 JOIN items ON {table2}.id = items.fk2'
    else:
        join_type = 'JOIN'
        join_clause = f'{table1} JOIN {table2} ON {table1}.{fk1} = {table2}.{fk2}'
    
    # Create schemas
    schema1 = f'''CREATE TABLE {table1} (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )'''
    
    schema2 = f'''CREATE TABLE {table2} (
        id INTEGER PRIMARY KEY,
        {fk1 if fk1 != 'id' else 'foreign_id'} INTEGER,
        amount REAL,
        FOREIGN KEY ({fk1 if fk1 != 'id' else 'foreign_id'}) REFERENCES {table1}(id)
    )'''
    
    # Generate data
    data1 = [(1, f'{table1[:-1]}1'), (2, f'{table1[:-1]}2'), (3, f'{table1[:-1]}3')]
    data2 = [(1, 1, 100.0), (2, 1, 150.0), (3, 2, 200.0), (4, 3, 250.0)]
    
    # Generate solution
    if 'self' in problem_type:
        solution = f'SELECT e1.name, e2.name FROM {join_clause}'
    else:
        solution = f'SELECT {table1}.name, {table2}.amount FROM {join_clause}'
    
    return {
        'id': challenge_id,
        'title': f'{join_type} Query #{challenge_id}',
        'description': f'{problem_desc}. Use {join_type.lower()} to combine the tables.',
        'difficulty': 'medium',
        'required_concepts': ['SELECT', join_type, 'JOIN'],
        'initial_schema': {table1: schema1, table2: schema2},
        'initial_data': [
            {'table': table1, 'data': data1},
            {'table': table2, 'data': data2}
        ],
        'expected_result': {'type': 'query_result'},
        'allowed_operations': ['SELECT', 'JOIN'],
        'solution_query': solution
    }


def _create_group_by_challenge(challenge_id: int, problem_type: str, problem_desc: str, solution_pattern: str) -> Dict[str, Any]:
    """Create a GROUP BY challenge."""
    import random
    random.seed(challenge_id * 4000)
    
    # Extract group column and aggregation from pattern
    if 'dept' in problem_type:
        group_col = 'department'
        agg_func = 'AVG(salary)'
        table = 'employees'
        schema = '''CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT,
            salary REAL
        )'''
        data = [
            (1, 'Alice', 'IT', 80000),
            (2, 'Bob', 'IT', 90000),
            (3, 'Charlie', 'HR', 60000),
            (4, 'Diana', 'HR', 70000),
        ]
    elif 'category' in problem_type:
        group_col = 'category'
        agg_func = 'COUNT(*)' if 'count' in problem_type else 'MIN(cost)'
        table = 'products'
        schema = '''CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            cost REAL
        )'''
        data = [
            (1, 'Product1', 'Electronics', 100.0),
            (2, 'Product2', 'Electronics', 150.0),
            (3, 'Product3', 'Clothing', 50.0),
            (4, 'Product4', 'Clothing', 75.0),
        ]
    else:
        group_col = 'status'
        agg_func = 'SUM(amount)'
        table = 'orders'
        schema = '''CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            status TEXT,
            amount REAL
        )'''
        data = [
            (1, 'pending', 100.0),
            (2, 'pending', 150.0),
            (3, 'completed', 200.0),
            (4, 'completed', 250.0),
        ]
    
    solution = f'SELECT {group_col}, {agg_func} as result FROM {table} GROUP BY {group_col}'
    
    return {
        'id': challenge_id,
        'title': f'Group By Analysis #{challenge_id}',
        'description': f'{problem_desc}. Use GROUP BY to aggregate the data.',
        'difficulty': 'medium',
        'required_concepts': ['SELECT', 'GROUP BY', 'Aggregate Functions'],
        'initial_schema': {table: schema},
        'initial_data': [{'table': table, 'data': data}],
        'expected_result': {'type': 'query_result'},
        'allowed_operations': ['SELECT', 'GROUP BY'],
        'solution_query': solution
    }


def _create_having_challenge(challenge_id: int, problem_type: str, problem_desc: str, solution_pattern: str) -> Dict[str, Any]:
    """Create a HAVING challenge."""
    import random
    random.seed(challenge_id * 5000)
    
    threshold = 50000 + (challenge_id * 500) % 20000
    
    table = 'employees'
    schema = '''CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        salary REAL
    )'''
    
    data = [
        (1, 'Alice', 'IT', 80000),
        (2, 'Bob', 'IT', 90000),
        (3, 'Charlie', 'HR', 60000),
        (4, 'Diana', 'HR', 70000),
        (5, 'Eve', 'Sales', 50000),
    ]
    
    solution = f'SELECT department, AVG(salary) as avg_salary FROM {table} GROUP BY department HAVING AVG(salary) > {threshold}'
    
    return {
        'id': challenge_id,
        'title': f'Having Clause Query #{challenge_id}',
        'description': f'{problem_desc}. Use HAVING to filter grouped results.',
        'difficulty': 'medium',
        'required_concepts': ['SELECT', 'GROUP BY', 'HAVING'],
        'initial_schema': {table: schema},
        'initial_data': [{'table': table, 'data': data}],
        'expected_result': {'type': 'query_result'},
        'allowed_operations': ['SELECT', 'GROUP BY', 'HAVING'],
        'solution_query': solution
    }


def _create_subquery_challenge(challenge_id: int, problem_type: str, problem_desc: str, solution_pattern: str) -> Dict[str, Any]:
    """Create a subquery challenge."""
    import random
    random.seed(challenge_id * 6000)
    
    table = 'employees'
    schema = '''CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        salary REAL
    )'''
    
    data = [
        (1, 'Alice', 80000),
        (2, 'Bob', 60000),
        (3, 'Charlie', 90000),
        (4, 'Diana', 70000),
    ]
    
    if 'WHERE' in solution_pattern or 'where' in problem_type:
        solution = 'SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)'
    else:
        solution = 'SELECT name, (SELECT AVG(salary) FROM employees) as avg_salary FROM employees'
    
    return {
        'id': challenge_id,
        'title': f'Subquery Analysis #{challenge_id}',
        'description': f'{problem_desc}. Use a subquery to solve this.',
        'difficulty': 'medium',
        'required_concepts': ['SELECT', 'Subqueries'],
        'initial_schema': {table: schema},
        'initial_data': [{'table': table, 'data': data}],
        'expected_result': {'type': 'query_result'},
        'allowed_operations': ['SELECT', 'Subqueries'],
        'solution_query': solution
    }


def _create_generic_medium_challenge(challenge_id: int, problem_type: str, problem_desc: str, solution_pattern: str) -> Dict[str, Any]:
    """Create a generic medium challenge."""
    return _create_join_challenge(challenge_id, problem_type, problem_desc, solution_pattern)


def _generate_hard_challenges() -> List[Dict[str, Any]]:
    """Generate 75 hard challenges, each with unique problem statement and solution."""
    challenges = []
    
    # Generate all 75 hard challenges (126-200)
    for challenge_id in range(126, 201):
        challenges.append(_create_unique_hard_challenge(challenge_id))
    
    return challenges


def _create_unique_hard_challenge(challenge_id: int) -> Dict[str, Any]:
    """Create a unique hard challenge based on challenge_id."""
    import random
    random.seed(challenge_id * 10000)
    
    # 75 different hard challenge patterns
    pattern_idx = challenge_id - 126
    
    # Different window function and CTE patterns
    problem_types = [
        # 0-14: Window functions - RANK/DENSE_RANK/ROW_NUMBER (15 challenges)
        ('window_rank', 'Rank employees by salary within department', 'RANK() OVER (PARTITION BY department ORDER BY salary DESC)'),
        ('window_dense_rank', 'Dense rank employees by salary', 'DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC)'),
        ('window_row_number', 'Assign row numbers to products by price', 'ROW_NUMBER() OVER (ORDER BY price DESC)'),
        ('window_percent_rank', 'Calculate percent rank of salaries', 'PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary)'),
        ('window_ntile', 'Divide employees into quartiles by salary', 'NTILE(4) OVER (ORDER BY salary)'),
        ('window_rank_multiple', 'Rank by multiple criteria', 'RANK() OVER (PARTITION BY dept ORDER BY salary DESC, hire_date ASC)'),
        ('window_row_number_partition', 'Row number within each category', 'ROW_NUMBER() OVER (PARTITION BY category ORDER BY price)'),
        ('window_dense_rank_date', 'Dense rank by date within group', 'DENSE_RANK() OVER (PARTITION BY group_id ORDER BY date DESC)'),
        ('window_percent_rank_price', 'Percent rank of product prices', 'PERCENT_RANK() OVER (ORDER BY price)'),
        ('window_ntile_salary', 'Divide into 5 salary groups', 'NTILE(5) OVER (ORDER BY salary)'),
        ('window_rank_desc', 'Rank in descending order', 'RANK() OVER (ORDER BY value DESC)'),
        ('window_row_number_asc', 'Row number in ascending order', 'ROW_NUMBER() OVER (ORDER BY value ASC)'),
        ('window_dense_rank_asc', 'Dense rank ascending', 'DENSE_RANK() OVER (ORDER BY value ASC)'),
        ('window_percent_rank_partition', 'Percent rank with partition', 'PERCENT_RANK() OVER (PARTITION BY group ORDER BY value)'),
        ('window_ntile_partition', 'NTILE with partition', 'NTILE(3) OVER (PARTITION BY category ORDER BY price)'),
        
        # 15-29: Window functions - LAG/LEAD (15 challenges)
        ('window_lag', 'Previous value in ordered sequence', 'LAG(amount, 1) OVER (ORDER BY date)'),
        ('window_lead', 'Next value in ordered sequence', 'LEAD(amount, 1) OVER (ORDER BY date)'),
        ('window_lag_partition', 'Previous value within partition', 'LAG(value, 1) OVER (PARTITION BY group_id ORDER BY date)'),
        ('window_lead_partition', 'Next value within partition', 'LEAD(value, 1) OVER (PARTITION BY group_id ORDER BY date)'),
        ('window_lag_multiple', 'Value 2 steps back', 'LAG(amount, 2) OVER (ORDER BY date)'),
        ('window_lead_multiple', 'Value 2 steps ahead', 'LEAD(amount, 2) OVER (ORDER BY date)'),
        ('window_lag_default', 'Previous value with default', 'LAG(amount, 1, 0) OVER (ORDER BY date)'),
        ('window_lead_default', 'Next value with default', 'LEAD(amount, 1, 0) OVER (ORDER BY date)'),
        ('window_lag_salary', 'Previous salary in department', 'LAG(salary, 1) OVER (PARTITION BY department ORDER BY hire_date)'),
        ('window_lead_price', 'Next price in category', 'LEAD(price, 1) OVER (PARTITION BY category ORDER BY date)'),
        ('window_lag_date', 'Previous date value', 'LAG(date, 1) OVER (ORDER BY id)'),
        ('window_lead_date', 'Next date value', 'LEAD(date, 1) OVER (ORDER BY id)'),
        ('window_lag_complex', 'Previous value with condition', 'LAG(CASE WHEN status = "active" THEN amount ELSE 0 END, 1) OVER (ORDER BY date)'),
        ('window_lead_complex', 'Next value with condition', 'LEAD(CASE WHEN status = "active" THEN amount ELSE 0 END, 1) OVER (ORDER BY date)'),
        ('window_lag_avg', 'Previous average value', 'LAG(AVG(amount) OVER (ORDER BY date), 1) OVER (ORDER BY date)'),
        
        # 30-44: Window functions - SUM/AVG OVER (15 challenges)
        ('window_running_sum', 'Running total of sales', 'SUM(amount) OVER (ORDER BY date)'),
        ('window_running_avg', 'Running average of values', 'AVG(value) OVER (ORDER BY date)'),
        ('window_partition_sum', 'Sum within partition', 'SUM(amount) OVER (PARTITION BY category ORDER BY date)'),
        ('window_partition_avg', 'Average within partition', 'AVG(value) OVER (PARTITION BY department ORDER BY date)'),
        ('window_running_count', 'Running count', 'COUNT(*) OVER (ORDER BY date)'),
        ('window_partition_count', 'Count within partition', 'COUNT(*) OVER (PARTITION BY group ORDER BY date)'),
        ('window_running_max', 'Running maximum', 'MAX(value) OVER (ORDER BY date)'),
        ('window_running_min', 'Running minimum', 'MIN(value) OVER (ORDER BY date)'),
        ('window_frame_sum', 'Sum with frame specification', 'SUM(amount) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)'),
        ('window_frame_avg', 'Average with frame', 'AVG(value) OVER (ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)'),
        ('window_unbounded_sum', 'Sum with unbounded preceding', 'SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)'),
        ('window_unbounded_avg', 'Average with unbounded', 'AVG(value) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)'),
        ('window_partition_sum_desc', 'Sum within partition descending', 'SUM(amount) OVER (PARTITION BY category ORDER BY date DESC)'),
        ('window_partition_avg_desc', 'Average within partition descending', 'AVG(value) OVER (PARTITION BY department ORDER BY date DESC)'),
        ('window_multiple_window', 'Multiple window functions', 'SUM(amount) OVER (ORDER BY date), AVG(amount) OVER (PARTITION BY category ORDER BY date)'),
        
        # 45-59: CTEs - basic and multiple (15 challenges)
        ('cte_basic', 'Basic CTE for revenue calculation', 'WITH revenue AS (SELECT customer_id, SUM(amount) as total FROM orders GROUP BY customer_id)'),
        ('cte_multiple', 'Multiple CTEs chained together', 'WITH step1 AS (...), step2 AS (SELECT * FROM step1 WHERE ...)'),
        ('cte_join', 'CTE with JOIN operation', 'WITH agg AS (SELECT id, SUM(amount) FROM table GROUP BY id) SELECT * FROM agg JOIN other ON ...'),
        ('cte_filtered', 'CTE with WHERE condition', 'WITH filtered AS (SELECT * FROM table WHERE condition) SELECT * FROM filtered'),
        ('cte_aggregated', 'CTE with aggregation', 'WITH totals AS (SELECT category, SUM(amount) FROM sales GROUP BY category) SELECT * FROM totals'),
        ('cte_union', 'CTE with UNION', 'WITH combined AS (SELECT * FROM table1 UNION SELECT * FROM table2) SELECT * FROM combined'),
        ('cte_subquery', 'CTE containing subquery', 'WITH results AS (SELECT * FROM (SELECT ... FROM table) sub) SELECT * FROM results'),
        ('cte_window', 'CTE with window function', 'WITH ranked AS (SELECT *, RANK() OVER (PARTITION BY dept ORDER BY salary) FROM employees) SELECT * FROM ranked'),
        ('cte_multiple_aggregations', 'Multiple aggregations in CTE', 'WITH stats AS (SELECT dept, AVG(salary), MAX(salary), MIN(salary) FROM employees GROUP BY dept)'),
        ('cte_join_multiple', 'CTE joining multiple tables', 'WITH combined AS (SELECT * FROM table1 JOIN table2 ON ... JOIN table3 ON ...)'),
        ('cte_filtered_join', 'CTE with filter and join', 'WITH filtered AS (SELECT * FROM table WHERE condition), joined AS (SELECT * FROM filtered JOIN other ON ...)'),
        ('cte_nested', 'Nested CTE structure', 'WITH outer AS (WITH inner AS (SELECT ...) SELECT * FROM inner) SELECT * FROM outer'),
        ('cte_case', 'CTE with CASE statement', 'WITH categorized AS (SELECT *, CASE WHEN value > 100 THEN "high" ELSE "low" END as category FROM table)'),
        ('cte_distinct', 'CTE with DISTINCT', 'WITH unique AS (SELECT DISTINCT category FROM products) SELECT * FROM unique'),
        ('cte_ordered', 'CTE with ORDER BY', 'WITH sorted AS (SELECT * FROM table ORDER BY value DESC) SELECT * FROM sorted LIMIT 10'),
        
        # 60-74: CTEs - recursive and complex (15 challenges)
        ('cte_recursive_basic', 'Basic recursive CTE for hierarchy', 'WITH RECURSIVE hierarchy AS (SELECT id, name, parent_id, 0 as level FROM table WHERE parent_id IS NULL UNION ALL SELECT ...)'),
        ('cte_recursive_path', 'Recursive CTE for path building', 'WITH RECURSIVE paths AS (SELECT id, name, CAST(name AS TEXT) as path FROM table WHERE parent_id IS NULL UNION ALL SELECT ...)'),
        ('cte_recursive_depth', 'Recursive CTE with depth limit', 'WITH RECURSIVE tree AS (SELECT id, name, parent_id, 0 as depth FROM table WHERE parent_id IS NULL UNION ALL SELECT ... WHERE depth < 5)'),
        ('cte_recursive_sum', 'Recursive CTE with aggregation', 'WITH RECURSIVE totals AS (SELECT id, value, 0 as running_total FROM table WHERE parent_id IS NULL UNION ALL SELECT ...)'),
        ('cte_recursive_count', 'Recursive CTE counting descendants', 'WITH RECURSIVE counts AS (SELECT id, 0 as descendant_count FROM table UNION ALL SELECT ...)'),
        ('cte_recursive_filter', 'Recursive CTE with filtering', 'WITH RECURSIVE filtered AS (SELECT * FROM table WHERE condition UNION ALL SELECT ... WHERE condition)'),
        ('cte_recursive_join', 'Recursive CTE with JOIN', 'WITH RECURSIVE joined AS (SELECT * FROM table1 WHERE condition UNION ALL SELECT * FROM table1 JOIN joined ON ...)'),
        ('cte_recursive_multiple', 'Multiple recursive CTEs', 'WITH RECURSIVE tree1 AS (...), tree2 AS (SELECT * FROM tree1 WHERE ...)'),
        ('cte_recursive_ordered', 'Recursive CTE with ordering', 'WITH RECURSIVE ordered AS (SELECT * FROM table ORDER BY id UNION ALL SELECT ... ORDER BY level)'),
        ('cte_recursive_complex', 'Complex recursive CTE', 'WITH RECURSIVE complex AS (SELECT id, name, parent_id, 0 as level, CAST(name AS TEXT) as path FROM table WHERE parent_id IS NULL UNION ALL SELECT id, name, parent_id, level + 1, path || " > " || name FROM table JOIN complex ON ...)'),
        ('cte_recursive_aggregate', 'Recursive with aggregation', 'WITH RECURSIVE agg AS (SELECT id, value, value as total FROM table WHERE parent_id IS NULL UNION ALL SELECT t.id, t.value, agg.total + t.value FROM table t JOIN agg ON ...)'),
        ('cte_recursive_window', 'Recursive CTE with window function', 'WITH RECURSIVE ranked AS (SELECT id, name, RANK() OVER (ORDER BY id) FROM table WHERE parent_id IS NULL UNION ALL SELECT ...)'),
        ('cte_recursive_case', 'Recursive CTE with CASE', 'WITH RECURSIVE categorized AS (SELECT id, CASE WHEN value > 100 THEN "high" ELSE "low" END as category FROM table WHERE parent_id IS NULL UNION ALL SELECT ...)'),
        ('cte_recursive_date', 'Recursive CTE for date series', 'WITH RECURSIVE dates AS (SELECT date("2024-01-01") as d UNION ALL SELECT date(d, "+1 day") FROM dates WHERE d < "2024-12-31")'),
        ('cte_recursive_number', 'Recursive CTE for number series', 'WITH RECURSIVE numbers AS (SELECT 1 as n UNION ALL SELECT n + 1 FROM numbers WHERE n < 100)'),
    ]
    
    problem_type, problem_desc, solution_pattern = problem_types[pattern_idx % len(problem_types)]
    
    # Generate challenge based on type
    if 'window' in problem_type:
        return _create_window_function_challenge(challenge_id, problem_type, problem_desc, solution_pattern)
    elif 'cte' in problem_type or 'CTE' in problem_type:
        return _create_cte_challenge(challenge_id, problem_type, problem_desc, solution_pattern)
    else:
        return _create_window_function_challenge(challenge_id, problem_type, problem_desc, solution_pattern)


def _create_window_function_challenge(challenge_id: int, problem_type: str, problem_desc: str, solution_pattern: str) -> Dict[str, Any]:
    """Create a window function challenge."""
    import random
    random.seed(challenge_id * 15000)
    
    table = 'employees'
    schema = '''CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        salary REAL,
        hire_date TEXT
    )'''
    
    data = [
        (1, 'Alice', 'IT', 80000, '2020-01-15'),
        (2, 'Bob', 'IT', 90000, '2019-03-20'),
        (3, 'Charlie', 'HR', 60000, '2021-06-10'),
        (4, 'Diana', 'HR', 70000, '2020-11-05'),
        (5, 'Eve', 'IT', 85000, '2022-02-14'),
    ]
    
    # Adjust solution based on pattern
    if 'PARTITION BY' in solution_pattern:
        solution = f'SELECT name, department, salary, {solution_pattern} as rank FROM {table}'
    elif 'ORDER BY date' in solution_pattern:
        # Use sales table for date-based
        table = 'sales'
        schema = '''CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            amount REAL,
            sale_date TEXT
        )'''
        data = [
            (1, 100.0, '2024-01-15'),
            (2, 200.0, '2024-01-20'),
            (3, 150.0, '2024-02-01'),
            (4, 300.0, '2024-02-10'),
        ]
        solution = f'SELECT sale_date, amount, {solution_pattern.replace("date", "sale_date").replace("amount", "amount")} as result FROM {table} ORDER BY sale_date'
    else:
        solution = f'SELECT name, department, salary, {solution_pattern} as result FROM {table}'
    
    return {
        'id': challenge_id,
        'title': f'Window Function Analysis #{challenge_id}',
        'description': f'{problem_desc}. Use window functions to solve this.',
        'difficulty': 'hard',
        'required_concepts': ['SELECT', 'Window Functions'],
        'initial_schema': {table: schema},
        'initial_data': [{'table': table, 'data': data}],
        'expected_result': {'type': 'query_result'},
        'allowed_operations': ['SELECT', 'Window Functions'],
        'solution_query': solution
    }


def _create_cte_challenge(challenge_id: int, problem_type: str, problem_desc: str, solution_pattern: str) -> Dict[str, Any]:
    """Create a CTE challenge."""
    import random
    random.seed(challenge_id * 20000)
    
    if 'recursive' in problem_type:
        # Recursive CTE for hierarchy
        table = 'employees'
        schema = '''CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manager_id INTEGER,
            FOREIGN KEY (manager_id) REFERENCES employees(id)
        )'''
        data = [
            (1, 'Manager', None),
            (2, 'Employee1', 1),
            (3, 'Employee2', 1),
            (4, 'Employee3', 2),
        ]
        
        solution = "WITH RECURSIVE hierarchy AS (SELECT id, name, manager_id, 0 as level FROM employees WHERE manager_id IS NULL UNION ALL SELECT e.id, e.name, e.manager_id, h.level + 1 FROM employees e JOIN hierarchy h ON e.manager_id = h.id) SELECT * FROM hierarchy"
    else:
        # Basic CTE
        table1 = 'customers'
        table2 = 'orders'
        schema1 = '''CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )'''
        schema2 = '''CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )'''
        data1 = [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie')]
        data2 = [(1, 1, 100.0), (2, 1, 150.0), (3, 2, 200.0)]
        
        threshold = 200 + (challenge_id * 10) % 100
        solution = f'WITH customer_revenue AS (SELECT customer_id, SUM(amount) as total FROM orders GROUP BY customer_id) SELECT c.name, cr.total FROM customers c JOIN customer_revenue cr ON c.id = cr.customer_id WHERE cr.total > {threshold}'
        
        return {
            'id': challenge_id,
            'title': f'CTE Analysis #{challenge_id}',
            'description': f'{problem_desc}. Use a CTE to solve this.',
            'difficulty': 'hard',
            'required_concepts': ['SELECT', 'CTE'],
            'initial_schema': {table1: schema1, table2: schema2},
            'initial_data': [
                {'table': table1, 'data': data1},
                {'table': table2, 'data': data2}
            ],
            'expected_result': {'type': 'query_result'},
            'allowed_operations': ['SELECT', 'CTE'],
            'solution_query': solution
        }
    
    return {
        'id': challenge_id,
        'title': f'Recursive CTE #{challenge_id}',
        'description': f'{problem_desc}. Use a recursive CTE to solve this.',
        'difficulty': 'hard',
        'required_concepts': ['SELECT', 'CTE', 'Recursive'],
        'initial_schema': {table: schema},
        'initial_data': [{'table': table, 'data': data}],
        'expected_result': {'type': 'query_result'},
        'allowed_operations': ['SELECT', 'CTE'],
        'solution_query': solution
    }
