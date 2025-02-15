def create_node_query(tx, board: str, game_state: str, parent_id, turn: str):
    # Создание узла
    query = """
        CREATE (n:Node 
        {
            board: $board,
            game_state: $game_state,
            visits: 0, 
            white_wins: 0, 
            black_wins: 0
        })
        RETURN elementId(n) AS node_id
        """
    result = tx.run(query, board=board, game_state=game_state)

    # Создание дуги от родителя
    node_id = result.single()["node_id"]
    if parent_id is not None:
        tx.run(
            """
        MATCH (parent:Node), (child:Node)
        WHERE elementId(parent) = $parent_id 
            AND elementId(child) = $child_id
        CREATE (parent)-[:CHILD {turn: $turn}]->(child)
        """,
            parent_id=parent_id,
            child_id=node_id,
            turn=turn,
        )

    return node_id


def find_node_by_board_query(tx, board: str):
    query = """
        MATCH (n:Node {state: $state})
        RETURN elementId(n) AS node_id
        """
    result = tx.run(query, state=board)
    record = result.single()
    return record["node_id"] if record else None


def get_children_query(tx, node_id):
    query = """
        MATCH (n:Node)-[:CHILD]->(child:Node)
        WHERE elementId(n) = $node_id
        RETURN 
            elementId(child) AS child_id, 
            child.state AS state, 
            child.visits AS visits, 
            child.white_wins AS white_wins, 
            child.black_wins AS black_wins
        """
    result = tx.run(query, node_id=node_id)
    return [
        {
            "id": record["child_id"],
            "state": record["state"],
            "visits": record["visits"],
            "white_wins": record["white_wins"],
            "black_wins": record["black_wins"],
        }
        for record in result
    ]


def get_parent_query(tx, node_id):
    query = """
        MATCH (parent:Node)-[:CHILD]->(n:Node)
        WHERE elementId(n) = $node_id
        RETURN elementId(parent) AS parent_id
        """
    result = tx.run(query, node_id=node_id)
    record = result.single()
    return record["parent_id"] if record else None


def increment_node_query(tx, node_id, white_wins, black_wins, visits):
    query = """
        MATCH (n:Node)
        WHERE elementId(n) = $node_id
        SET n.white_wins = n.white_wins + $white_wins,
            n.black_wins = n.black_wins + $black_wins,
            n.visits = n.visits + $visits
        """
    tx.run(
        query,
        node_id=node_id,
        white_wins=white_wins,
        black_wins=black_wins,
        visits=visits,
    )


def get_best_move_query(tx, root_id, is_white_turn):
    query = """
        MATCH (root:Node)-[r:CHILD]->(child:Node)
        WHERE elementId(root) = $root_id AND child.visits > 0
        RETURN 
            r.turn AS turn, 
            child.visits AS visits, 
            CASE WHEN $is_white_turn THEN child.white_wins 
                 ELSE child.black_wins END AS wins
        ORDER BY wins / visits DESC
        LIMIT 1
        """
    result = tx.run(query, root_id=root_id, is_white_turn=is_white_turn)
    record = result.single()
    if record:
        return record["turn"]
    return None
