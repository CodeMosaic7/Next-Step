from google.cloud import aiplatform
PROJECT_ID = "your-project-id"
REGION = "us-central1"  # or your preferred region
aiplatform.init(project=PROJECT_ID, location=REGION)

# Create the Vector Search Index
my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name="my-vector-index",
    contents_delta_uri=BUCKET_URI,
    dimensions=768,  # must match your embeddings
    approximate_neighbors_count=100
)

# Deploy the Index via an Endpoint
my_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name="my-vector-endpoint",
    public_endpoint_enabled=True
)
my_endpoint.deploy_index(index=my_index, deployed_index_id="deployed-index-id")
