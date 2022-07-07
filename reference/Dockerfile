FROM python:3.8
ADD bash_dir/_reference.sh /
RUN ["chmod", "+x", "./_reference.sh"]
RUN pip install pandas
RUN pip install csvkit
CMD ./_reference.sh
