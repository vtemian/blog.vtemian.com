---
title: "{{ .Title }}"
date: {{ .PublishDate.Format "2006-01-02" }}
author: {{ .Site.Params.author }}
url: {{ .Permalink }}
{{- with .Description }}
description: "{{ . }}"
{{- end }}
{{- with .Params.tags }}
tags: [{{ delimit . ", " }}]
{{- end }}
{{- with .Params.event }}
event: "{{ . }}"
{{- end }}
{{- with .Params.event_url }}
event_url: {{ . }}
{{- end }}
{{- with .Params.slides }}
slides: {{ . }}
{{- end }}
{{- with .Params.video }}
video: {{ . }}
{{- end }}
---

# {{ .Title }}

{{ .RawContent }}
