"""Plugin for retrieving and formatting citations from Bing search."""

import json
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class CitationLoggerPlugin:
    """A plugin for retrieving and formatting citations from Bing search."""
    
    def __init__(self, connection_string=None):
        """Initialize the plugin.
        
        Args:
            connection_string: Not used but kept for compatibility
        """
        self._cached_citations = {}  # Cache citations by thread_id
    
    @kernel_function(description="Get citations from thread and format as markdown")
    def get_formatted_citations(self, thread_id: str) -> str:
        """Retrieve citations from a thread and return as formatted markdown.
        
        Args:
            thread_id: The thread ID to retrieve citations from
            
        Returns:
            str: JSON string with the citations and formatted markdown
        """
        try:
            # Step 1: Retrieve the citations from the thread (cached)
            citations = self._get_citations_from_thread(thread_id)

            # Step 2: Format the citations as markdown
            markdown = self._format_citations_as_markdown(citations)

            # Return the results
            return json.dumps({
                "success": True,
                "citation_count": len(citations),
                "citations": citations,
                "markdown": markdown
            })
        except Exception as e:
            print(f"Error in get_formatted_citations: {e}")
            import traceback
            traceback.print_exc()
            return json.dumps({
                "error": str(e),
                "success": False,
                "citation_count": 0,
                "citations": [],
                "markdown": "### References\n\nUnable to retrieve citations."
            })
    
    def _get_citations_from_thread(self, thread_id):
        """Get citations from a thread.
        
        Args:
            thread_id: The thread ID from Azure AI Projects
        
        Returns:
            list: List of citation dictionaries
        """
        # Return cached citations if available
        if thread_id in self._cached_citations:
            return self._cached_citations[thread_id]

        # Without Azure project client access we cannot pull annotations from
        # remote assistant messages. Keep this lightweight: return empty list and
        # allow other parts of the app to populate _cached_citations when using
        # an external search provider.
        print(f"No cached citations for thread {thread_id}. Returning empty list.")
        return []
    
    def _extract_source_from_title(self, title):
        """Extract the source name from a citation title.
        
        Args:
            title: The citation title
            
        Returns:
            str: The extracted source name
        """
        # Many citation titles follow the format: "Title - Source, Date"
        if " - " in title:
            parts = title.split(" - ")
            if len(parts) > 1:
                source_part = parts[-1].strip()
                # Further extract if there's a comma with date
                if "," in source_part:
                    return source_part.split(",")[0].strip()
                return source_part
        
        # Default to returning the title itself if no clear source
        return title
    
    def _format_citations_as_markdown(self, citations):
        """Format citations as markdown.
        
        Args:
            citations: List of citation dictionaries
            
        Returns:
            str: Formatted citation section as markdown
        """
        if not citations:
            return "### References\n\nNo citations available."
            
        citation_section = "### References\n\n"
        
        for i, citation in enumerate(citations):
            title = citation.get("title", "Unknown Source")
            url = citation.get("url", "#")
            source = citation.get("source", "Unknown")
            
            citation_section += f"{i+1}. [\"{title}\" - {source}]({url})\n\n"
        
        return citation_section
    
    @kernel_function(description="Enhance political risk output with citations")
    def enhance_political_risk_output(self, agent_output: str, thread_id: str) -> str:
        """Enhances the political risk output by adding proper citations.
        
        Args:
            agent_output: The agent's output content
            thread_id: The thread ID to retrieve citations from
            
        Returns:
            str: Enhanced output with proper citations
        """
        try:
            # Get the citations from the thread
            citations = self._get_citations_from_thread(thread_id)
            
            if not citations:
                print("No citations found, returning original output")
                return agent_output
            
            # Check if the output already has a References section
            if "### References" in agent_output:
                print("Output already has References section, replacing it")
                
                # Replace the existing References section
                import re
                pattern = r'### References.*?(?=###|\Z)'
                references_section = self._format_citations_as_markdown(citations)
                enhanced_output = re.sub(pattern, references_section, agent_output, flags=re.DOTALL)
                
                return enhanced_output
            else:
                # Add the References section at the end
                print("Adding References section to output")
                references_section = self._format_citations_as_markdown(citations)
                
                # Make sure there's a newline before adding references
                if not agent_output.endswith("\n\n"):
                    enhanced_output = agent_output + "\n\n" + references_section
                else:
                    enhanced_output = agent_output + references_section
                
                return enhanced_output
                
        except Exception as e:
            print(f"Error enhancing political risk output: {e}")
            import traceback
            traceback.print_exc()
            return agent_output  # Return original output in case of error