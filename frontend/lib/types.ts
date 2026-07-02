export type FeatureInfo = {
  feature_id: string;
  label: string;
  description: string;
  required_files: boolean;
  output_type: string;
  visible_to_customer: boolean;
  confirm_before_execute: boolean;
};

export type UploadedFile = {
  file_id: string;
  filename: string;
  content_type?: string;
  size_bytes: number;
};

export type ChatResponse = {
  conversation_id: string;
  message: string;
  mode: string;
};

export type TaskCreateResponse = {
  task_id: string;
  status: string;
  feature_id: string;
  skill: string;
  message: string;
};

export type TaskResult = {
  task_id: string;
  status: string;
  feature_id: string;
  skill: string;
  output_text?: string;
  output_files: string[];
  error?: string;
};
