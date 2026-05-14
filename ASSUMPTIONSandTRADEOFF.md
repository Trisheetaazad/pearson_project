## 📝 Assumptions & Trade-offs

### Assumptions
* **Completeness First**: We assume the user prioritizes data completeness over processing speed. In legal contexts, missing a single clause is more costly than waiting a few extra seconds for processing.
* **Visual Reliability**: We assume that PDFs may contain "hidden" or broken digital text layers that do not match the visual content. Treating every page as an image is the only way to ensure 100% data fidelity.

### Trade-offs
* **Strict OCR vs. CPU**: Forcing OCR on every page is significantly more CPU-intensive than digital extraction. However, this trade-off provides the reliability required for legal-grade document recovery.
* **Embedding Efficiency**: We use a lightweight embedding model (**all-MiniLM-L6-v2**). This allows for fast local processing on standard hardware while maintaining the high retrieval accuracy necessary for RAG-based summaries.