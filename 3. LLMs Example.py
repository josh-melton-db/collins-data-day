# Databricks notebook source
# MAGIC %md
# MAGIC We can't customize clusters in the sandbox to work with LLMs, so if you'd like to follow along with this example you can find the <a href="https://www.dbdemos.ai/demo-notebooks.html?demoName=llm-dolly-chatbot">notebooks here</a> or you can run the following commands in your environment

# COMMAND ----------

# MAGIC %pip install dbdemos

# COMMAND ----------

import dbdemos
dbdemos.install('llm-dolly-chatbot')
