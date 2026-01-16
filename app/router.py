from semantic_router import Route, SemanticRouter

from semantic_router.encoders import HuggingFaceEncoder

encoder=HuggingFaceEncoder(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

faq=Route(
    name="faq",
    utterances=[
        "What is the return policy of the products?",
        "Do I get a discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?"
    ],
    score_threshold=0.3
)

sql=Route(
    name="sql",
    utterances=[
        "I want to buy Nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of Puma running shoes?"
    ],
    score_threshold=0.3
)

router=SemanticRouter(
    encoder=encoder
)

router.add(routes=[faq,sql])
print(f"Router routes: {len(router.routes)}")
# Force local index usage style if needed, or check if index is populated
if router.index:
    print(f"Index type: {type(router.index)}")
    try:
        # Check if index has items. LocalIndex doesn't expose len easily but we can try
        pass 
    except:
        pass

if __name__ == "__main__":
    # query="Do I get a discount with the HDFC credit card?"
    # result=router(query)
    # print(result)
    print(router("Do I get a discount with the HDFC credit card?").name)
    print(router("I want to buy Nike shoes that have 50% discount.").name)
    print(router("What is the return policy of the products?").name)