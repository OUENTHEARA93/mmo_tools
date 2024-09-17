import { BaseOptions } from './BaseOptions';
import ActiveFilter from '/AdminLTE/ActiveFilter';
export interface Options extends BaseOptions {
    filter: ActiveFilter;
}
