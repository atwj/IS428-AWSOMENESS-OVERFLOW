from neo4j.v1 import GraphDatabase
uri = 'bolt://127.0.0.1:7687'
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

# Test if driver working
print(driver)

#
print(driver.close())
driver.close()