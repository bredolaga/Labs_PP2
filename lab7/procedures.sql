--procedure that insert new contact or change phone
create or replace procedure add_contact(new_name varchar, new_phone varchar)
as $$
begin
	if exists ( 
		select 1 from phonebook where name = new_name
		) then 
		update phonebook
		set phone = new_phone
		where name = new_name;
	else 
		insert into phonebook(name, phone)
		values (new_name, new_phone);
	end if;
end
$$ language plpgsql;

--procedure to insert many new users from list of name or phone
CREATE OR REPLACE PROCEDURE insert_many_contacts(names text[], phones text[])
AS $$
DECLARE
    i int;
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts(
        name text,
        phone text
    ) ON COMMIT DROP;

    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            INSERT INTO phonebook(name, phone)
            VALUES (names[i], phones[i]);
        ELSE
            INSERT INTO invalid_contacts(name, phone)
            VALUES (names[i], phones[i]);
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

--a procedure that delete data by name or phone
create or replace procedure delete_data(d_name text, d_phone text)
as $$
begin
	delete from phonebook
	where name = d_name or phone = d_phone;
end;
$$ language plpgsql 


