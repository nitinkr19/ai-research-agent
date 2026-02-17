// Helpers for rendering streamed research output nicely in the UI.
// - Strips markdown code-fences (```json ... ```)
// - Converts JSON blocks into readable bullet points
// - Renders **bold** spans

// Remove markdown fenced code-block markers like ```json ... ```
// Keeps the content, just strips the fence lines so it looks like normal text.
export const stripCodeFences = (text) => {
  if (!text) return text;
  return (
    text
      // opening fences (optionally with language), optionally prefixed by list markers like "- "
      .replace(/^\s*([-*+]\s*)?```[a-zA-Z0-9_-]*\s*$/gm, "")
      // closing fences, optionally prefixed by list markers like "- "
      .replace(/^\s*([-*+]\s*)?```\s*$/gm, "")
      // if the fence was in a list item like "- ```json", remove the now-empty bullet
      .replace(/^\s*[-*+]\s*$/gm, "")
      // collapse 3+ blank lines caused by stripping fences
      .replace(/\n{3,}/g, "\n\n")
  );
};

// Format JSON as bullet points, using **key** for object keys.
export const formatJsonAsBullets = (obj, indent = 0) => {
  if (Array.isArray(obj)) {
    if (obj.length === 0) return "[]";
    return obj
      .map((item) => {
        if (typeof item === "object" && item !== null) {
          return `${"  ".repeat(indent)}• ${formatJsonAsBullets(item, indent + 1)}`;
        }
        return `${"  ".repeat(indent)}• ${item}`;
      })
      .join("\n");
  }

  if (typeof obj === "object" && obj !== null) {
    const entries = Object.entries(obj);
    if (entries.length === 0) return "{}";
    return entries
      .map(([key, value]) => {
        if (typeof value === "object" && value !== null) {
          return `${"  ".repeat(indent)}• **${key}**:\n${formatJsonAsBullets(value, indent + 1)}`;
        }
        return `${"  ".repeat(indent)}• **${key}**: ${value}`;
      })
      .join("\n");
  }

  return String(obj);
};

// Find and replace JSON blocks in text (works with nested braces and streaming/incomplete JSON).
export const processJsonBlocks = (text) => {
  let startIndex = 0;
  const result = [];

  while (startIndex < text.length) {
    const openBrace = text.indexOf("{", startIndex);
    const openBracket = text.indexOf("[", startIndex);

    let jsonStart = -1;
    let openChar = "";
    let closeChar = "";

    if (openBrace !== -1 && (openBracket === -1 || openBrace < openBracket)) {
      jsonStart = openBrace;
      openChar = "{";
      closeChar = "}";
    } else if (openBracket !== -1) {
      jsonStart = openBracket;
      openChar = "[";
      closeChar = "]";
    }

    if (jsonStart === -1) {
      result.push(text.substring(startIndex));
      break;
    }

    // Add text before JSON
    result.push(text.substring(startIndex, jsonStart));

    // Find matching closing brace/bracket
    let depth = 0;
    let jsonEnd = -1;
    let inString = false;
    let escapeNext = false;

    for (let i = jsonStart; i < text.length; i++) {
      const char = text[i];

      if (escapeNext) {
        escapeNext = false;
        continue;
      }

      if (char === "\\") {
        escapeNext = true;
        continue;
      }

      if (char === '"' && !escapeNext) {
        inString = !inString;
        continue;
      }

      if (!inString) {
        if (char === openChar) {
          depth++;
        } else if (char === closeChar) {
          depth--;
          if (depth === 0) {
            jsonEnd = i + 1;
            break;
          }
        }
      }
    }

    if (jsonEnd !== -1) {
      const jsonStr = text.substring(jsonStart, jsonEnd);
      try {
        const jsonObj = JSON.parse(jsonStr);
        const bullets = formatJsonAsBullets(jsonObj);
        result.push("\n" + bullets + "\n");
        startIndex = jsonEnd;
      } catch {
        // Not valid JSON, keep original text
        result.push(jsonStr);
        startIndex = jsonEnd;
      }
    } else {
      // Incomplete JSON (streaming) — keep remaining text unchanged
      result.push(text.substring(jsonStart));
      break;
    }
  }

  return result.join("");
};

// Render markdown bold (**text**) into React nodes.
export const renderMarkdown = (text) => {
  const parts = [];
  let lastIndex = 0;
  const boldRegex = /\*\*(.*?)\*\*/g;
  let match;

  while ((match = boldRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }
    parts.push(
      <strong key={match.index} style={{ fontWeight: "600", color: "#000" }}>
        {match[1]}
      </strong>,
    );
    lastIndex = match.index + match[0].length;
  }

  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return parts.length > 0 ? parts : text;
};

// Render text nicely for the report view.
export const renderFormattedText = (text) => {
  let processedText = stripCodeFences(text);
  processedText = processJsonBlocks(processedText);

  const lines = processedText.split("\n");
  const result = [];

  lines.forEach((line, lineIdx) => {
    if (line.trim() === "") {
      result.push(
        <div key={lineIdx} style={{ marginBottom: "4px" }}>
          &nbsp;
        </div>,
      );
      return;
    }

    // Indent bullet lines (from JSON conversion)
    if (line.trim().startsWith("•")) {
      result.push(
        <div key={lineIdx} style={{ marginBottom: "6px", marginLeft: "20px" }}>
          {renderMarkdown(line)}
        </div>,
      );
      return;
    }

    result.push(
      <div key={lineIdx} style={{ marginBottom: "4px" }}>
        {renderMarkdown(line)}
      </div>,
    );
  });

  return result;
};

