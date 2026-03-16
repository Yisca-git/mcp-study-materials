"""Sample usage of the Study Materials MCP Server."""

from main import StudyMaterialMCPServer


def main():
    """Demonstrate server capabilities."""
    print("=" * 70)
    print("Study Materials MCP Server - Sample Usage")
    print("=" * 70)
    
    # Initialize server
    server = StudyMaterialMCPServer()
    
    # Test 1: Get available tools
    print("\n[1] Available Tools:")
    print("-" * 70)
    tools = server.get_tools()
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}")
        print(f"   Description: {tool['description']}")
    
    # Test 2: List topics
    print("\n[2] List Topics:")
    print("-" * 70)
    result = server.call_tool("list_topics")
    if result['success']:
        topics = result['data']['topics']
        if topics:
            print(f"Found {result['data']['count']} topics:")
            for topic in topics[:10]:
                print(f"  - {topic}")
            if len(topics) > 10:
                print(f"  ... and {len(topics) - 10} more")
        else:
            print("No topics found. Add study materials to study_materials/ directory.")
    else:
        print(f"Error: {result['error']['message']}")
    
    # Test 3: Search materials
    print("\n[3] Search Materials:")
    print("-" * 70)
    queries = ["algebra", "mathematics", "learning"]
    for query in queries:
        result = server.call_tool("search_material", query=query, top_k=3)
        if result['success']:
            count = result['data']['results_count']
            print(f"Query: '{query}' - Found {count} results")
            if count > 0:
                for i, res in enumerate(result['data']['results'][:2], 1):
                    print(f"  {i}. {res['filename']} (score: {res['relevance_score']:.2f})")
                    if res['snippets']:
                        snippet = res['snippets'][0][:100] + "..." if len(res['snippets'][0]) > 100 else res['snippets'][0]
                        print(f"     Snippet: {snippet}")
        else:
            print(f"Error: {result['error']['message']}")
    
    # Test 4: Categorize documents
    print("\n[4] Document Categorization:")
    print("-" * 70)
    result = server.call_tool("categorize_documents")
    if result['success']:
        categorization = result['data']['categorization']
        if categorization:
            print(f"Found {result['data']['categories_count']} categories:")
            for category, info in categorization.items():
                print(f"  - {category}: {info['document_count']} document(s)")
        else:
            print("No documents to categorize.")
    else:
        print(f"Error: {result['error']['message']}")
    
    # Test 5: Rank documents
    print("\n[5] Document Importance Ranking:")
    print("-" * 70)
    result = server.call_tool("rank_documents")
    if result['success']:
        ranked = result['data']['ranked_documents']
        if ranked:
            print(f"Top {min(5, len(ranked))} documents by importance:")
            for doc in ranked[:5]:
                print(f"  {doc['filename']}")
                print(f"    Importance Score: {doc['importance_score']:.2f}")
                print(f"    Reasons: {', '.join(doc['reasons'])}")
        else:
            print("No documents to rank.")
    else:
        print(f"Error: {result['error']['message']}")
    
    # Test 6: Find knowledge gaps (if topics exist)
    print("\n[6] Knowledge Gap Analysis:")
    print("-" * 70)
    topics_result = server.call_tool("list_topics")
    if topics_result['success'] and topics_result['data']['topics']:
        sample_topic = topics_result['data']['topics'][0]
        result = server.call_tool("find_knowledge_gaps", query=sample_topic)
        if result['success']:
            print(f"Analysis for: '{sample_topic}'")
            print(f"  Confidence Level: {result['data']['confidence_level']:.2f}")
            print(f"  Covered Materials: {result['data']['covered_materials']}")
            print("  Gaps Identified:")
            for gap in result['data']['gaps_identified'][:3]:
                print(f"    - {gap}")
            print("  Recommendations:")
            for rec in result['data']['recommendations'][:3]:
                print(f"    - {rec}")
        else:
            print(f"Error: {result['error']['message']}")
    else:
        print("Add study materials to perform gap analysis.")
    
    print("\n" + "=" * 70)
    print("Sample Usage Complete!")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Add PDF/TXT/MD files to study_materials/ directory")
    print("2. Run this script again to see real results")
    print("3. Read README.md for detailed API documentation")
    print("4. Check QUICKSTART.md for more examples")


if __name__ == "__main__":
    main()
