-- 1. Процедура UPSERT (вставить или обновить, если уже есть)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_surname VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name AND surname = p_surname) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO contacts(name, surname, phone) VALUES(p_name, p_surname, p_phone);
    END IF;
END;
$$;

-- 2. Процедура массовой вставки (с валидацией телефонов)
-- INOUT параметр вернет список ошибочных записей
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names VARCHAR[],
    p_surnames VARCHAR[],
    p_phones VARCHAR[],
    INOUT invalid_entries TEXT[] DEFAULT '{}'
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    invalid_entries := '{}';
    FOR i IN 1 .. COALESCE(array_length(p_names, 1), 0) LOOP
        -- Проверка: телефон должен содержать от 10 до 15 цифр, может начинаться с +
        IF p_phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            CALL upsert_contact(p_names[i], p_surnames[i], p_phones[i]);
        ELSE
            invalid_entries := array_append(invalid_entries, p_names[i] || ' ' || p_surnames[i] || ' (' || p_phones[i] || ')');
        END IF;
    END LOOP;
END;
$$;

-- 3. Процедура удаления по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_identifier OR surname = p_identifier OR phone = p_identifier;
END;
$$;