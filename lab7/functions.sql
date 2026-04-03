-- func that return records that matched to some pattern
create or replace function find(pattern TEXT)
RETURNS TABLE (name varchar, phone varchar)
as $$
begin
	return query
	select c.name, c.phone
	from phonebook as c
	where c.name ilike '%' || pattern || '%'
	or c.phone ilike '%' || pattern || '%';
end;
$$ language plpgsql;

-- func thar queries data from table with pagination
create or replace function paginated_contacts(lim int, offs int)
RETURNS TABLE (id int, name varchar, phone varchar)
as $$
begin 
	return query
	select c.id, c.name, c.phone
	from phonebook as c
	order by c.id
	limit lim offset offs;
end;
$$ language plpgsql;
