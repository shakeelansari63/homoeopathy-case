export interface IDB {
    dbProtocol: string;
    dbPath: string;

    checkDbAccess(dbName: string) : boolean;
}