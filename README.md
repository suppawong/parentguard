# ParentGuard

This is the repository for the source code of the project FALCoN (Foul and Abusive Language detection using Co-training in social Networks), an intelligent framework for detecting and classifying abusive language, utilizing unlabeled data.

## Feature Extraction

This group of code handles extracting context features from each social media message. For content features, it uses TFIDF or UML-fit representations.

## Co-Training

This package has the code that performs the co-training pipeline, including finding the right combination of base classifiers and confidence probability windows. Two co-training modes are implemented: one supports incremental feedback of the pseudo-labeled data, and another allows the pseudo-labeled data to be re-labeled. 

## Evaluation

The evaluation code handles the evaluation protocol.

## Chrome Extension

The Chrome extension code implements the demo Chrome web plugin that provide guidance and monitor children while surfing on Facebook.