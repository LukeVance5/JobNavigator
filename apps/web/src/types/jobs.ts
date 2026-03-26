export interface Job {
  id: string;
  user_id: string;
  title: string;
  description: string;
  company: string | undefined;
  location: string | undefined;
  salary_range: string | undefined;
  created_at: Date | undefined;
  applied_at: Date;
  status: string;
}

export interface JobElement extends Job {
  summary: string;
  skills: string;
  yoe: string;
}

export interface JobFocusProp extends Job {
  discription: string;
  skills: string;
  yoe: string | undefined;
  benifits: string | undefined;
  url: string | undefined;
}
