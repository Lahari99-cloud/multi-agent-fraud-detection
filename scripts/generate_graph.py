from pipeline.graph import compiled_graph


png = compiled_graph.get_graph().draw_mermaid_png()

with open("docs/langgraph_pipeline.png", "wb") as f:
    f.write(png)

print("Saved graph visualization")