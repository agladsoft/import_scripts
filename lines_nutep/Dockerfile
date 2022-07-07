FROM python:3.8
ADD bash_dir/_nutep_lines.sh /
RUN ["chmod", "+x", "./_nutep_lines.sh"]
RUN pip install pandas
RUN pip install csvkit
CMD ./_nutep_lines.sh
