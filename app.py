from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith('.xlsx'):  # The file is an .xlsx file
                df = pd.read_excel(file)
            else:
                return render_template('upload.html', message='Invalid file type')

            # Remove all occurrences of '%' from the data
            df = df.replace('%','', regex=True)

            filename = os.path.splitext(os.path.basename(file.filename))[0].replace(' ', '_')
            fields = [field.replace('"', ' ').strip().replace(' ', '_').lstrip('%') for field in df.columns.tolist()]

            output = [f'Table {filename} {{']

            for field in fields:
                if "date" in field.lower():
                    output.append('\t' + field + " date")
                else:
                    output.append('\t' + field + " varchar")

            output.append('}')

            result = '\n'.join(output)
            return render_template('result.html', result=result)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
