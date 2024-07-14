# 类布局

```cpp
class MyWidget : public QWidget {
public:
  MyWidget(QWidget *parent);
  ~MyWidget();

  void publicFunc();

protected:
  // for outer
  virtual void protectedFunc();
  
private:
  // for inner
  void privateFunc();

  /* Qt Func */
protected:
  // for outer rewrite
  virtual void event(QEvent *event) override;

private:
  // for inner, no need to rewrite twice
  void mouseEvent(QMouseEvent *event) override;

  /* Local Variable */
public:
  int public_var;
  
protected:  
  int protected_var_;

private:
  int private_var_;
};

```
