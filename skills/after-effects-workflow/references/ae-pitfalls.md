# AE pitfalls observed in production

- `AfterFX.exe -r script.jsx` targets a normal running Windows AE instance. Launching against no instance or an instance started with `-m` can behave differently. Inspect active instances first; upstream offers a resident agent for multiple instances. Do not kill or restart the artist's AE without authorization.
- Modal dialogs block scripts. Read their actual text; use the MCP's dialog inspection/dismiss operation where supported. A save/discard decision belongs to the user. Bound retries and fix the cause rather than repeating the same script.
- Localized effect labels and property numbers are fragile. Log each property's `matchName` and `propertyValueType`, then address the correct value property. Radial Blur in the tested AE build has a leading `NO_VALUE` property: amount is `ADBE Radial Blur-0001`, not necessarily index1.
- AE's camera point of interest can be represented by `ADBE Anchor Point` in the transform group. Do not assume an invented match name exists.
- Check actual asset encoding when an import fails. A file named `.PNG` may contain another image format; lossless re-encoding into a genuine PNG fixes container mismatches without redesigning the image.
- Non-uniformly scaled grids become rectangles. Generate square vector cells, or scale the raster uniformly and crop it. Keep the grid below opaque product layers.
- A blanket Fill on a multicolor service icon destroys its internal details. Keep original color unless monochrome was explicitly requested; reserve tinting for genuinely monochrome assets.
- Animated rounded-card mask paths must keep compatible vertices and tangent arrays. Store width, height and radius in project notes; consider a native slider-driven expression for interactive tuning.
- Do not wait inside JSX for a newly written PNG to become visible through a reused `File` object. Export a bounded frame batch, write a completion marker, then check externally that every frame exists and is readable.
- Never replace an audio file while AE has it open. Write a new version, import/relink it and save.
- An AEP save marker proves execution, not design quality. User review and sampled frames provide visual evidence. Honor a request for native AE review without rendering.
- Retained AEPs may reference assets inside old version folders. Collect/relink footage before deleting those folders. Deleting an old render is different from deleting source media.

These are observed behaviors, not a complete API contract. Consult the installed tool's schemas and [upstream documentation](https://github.com/kumoproductions/mcp-aftereffects).
