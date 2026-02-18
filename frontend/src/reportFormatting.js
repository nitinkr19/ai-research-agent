import React from "react";

/**
 * Helpers for rendering streamed research report in the UI.
 * - Strips markdown code fences (e.g. ```json ... ```)
 * - Converts JSON blocks into bullet points
 * - Renders **bold** as <strong>
 */

export const stripCodeFences = (text) => {
  if (!text) return text;
  return text
    .replace(/^\s*([-*+]\s*)?```[a-zA-Z0-9_-]*\s*$/gm, "")
    .replace(/^\s*([-*+]\s*)?```\s*$/gm, "")
    .replace(/^\s*[-*+]\s*$/gm, "")
    .replace(/\n{3,}/g, "\n\n");
};

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

    result.push(text.substring(startIndex, jsonStart));

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
      if (char === '"') {
        inString = !inString;
        continue;
      }
      if (!inString) {
        if (char === openChar) depth++;
        else if (char === closeChar) {
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
        result.push("\n" + formatJsonAsBullets(jsonObj) + "\n");
        startIndex = jsonEnd;
      } catch {
        result.push(jsonStr);
        startIndex = jsonEnd;
      }
    } else {
      result.push(text.substring(jsonStart));
      break;
    }
  }

  return result.join("");
};

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
      </strong>
    );
    lastIndex = match.index + match[0].length;
  }

  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return parts.length > 0 ? parts : text;
};

export const renderFormattedReport = (text) => {
  let processed = stripCodeFences(text);
  processed = processJsonBlocks(processed);

  const lines = processed.split("\n");
  const result = [];

  lines.forEach((line, lineIdx) => {
    if (line.trim() === "") {
      result.push(
        <div key={lineIdx} style={{ marginBottom: "4px" }}>
          &nbsp;
        </div>
      );
      return;
    }
    if (line.trim().startsWith("•")) {
      result.push(
        <div key={lineIdx} style={{ marginBottom: "6px", marginLeft: "20px" }}>
          {renderMarkdown(line)}
        </div>
      );
    } else {
      result.push(
        <div key={lineIdx} style={{ marginBottom: "4px" }}>
          {renderMarkdown(line)}
        </div>
      );
    }
  });

  return result;
};
