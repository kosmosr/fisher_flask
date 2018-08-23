-- 触发器SQL
CREATE TRIGGER update_data
  AFTER UPDATE
  ON book
  FOR EACH ROW
  INSERT INTO book_update (isbn, status)
  SELECT NEW.isbn, 0 where NOT EXISTS (SELECT * FROM book_log WHERE isbn = NEW.isbn AND type != 1);