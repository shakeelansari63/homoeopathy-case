export interface Patient {
    id?: number;
    firstName: string;
    lastName: string;
    age: number;
    gender: string;
    phone: string;
    address: string;
    occupation: string;
    maritalStatus: string;
    reference: string;
    datetm?: Date;
}

export interface PatientState {
    patientsList: Patient[];
    newFormVisibe: boolean;
}