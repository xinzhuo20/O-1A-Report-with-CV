from jinja2 import Environment, FileSystemLoader

def generate_html_report(classification_result: dict, overall_rating: str, cv_text: str) -> str:
    """
    Generate an HTML report using the classification results, overall rating, and the extracted CV text.
    """
    # Set up the Jinja2 environment to load HTML templates from the "templates" folder
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    template = env.get_template("report_template.html")
    
    # Prepare data for the template
    data = {
        "overall_rating": overall_rating,
        "classification": dict(zip(classification_result["labels"], classification_result["scores"])),
        "cv_text": cv_text,
    }
    
    # Render and return the HTML content
    html_out = template.render(data)
    return html_out
