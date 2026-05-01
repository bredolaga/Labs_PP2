CREATE OR REPLACE FUNCTION unified_search(q TEXT)
RETURNS TABLE(contact_name VARCHAR, contact_email VARCHAR, contact_phone VARCHAR, phone_type VARCHAR, group_name VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email, p.phone, p.type, g.name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.name ILIKE '%' || q || '%'
       OR c.email ILIKE '%' || q || '%'
       OR p.phone ILIKE '%' || q || '%';
END;
$$;
