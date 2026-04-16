(set-logic ALL)
; Constraint ID: cb63f194c5cf795a
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59632)) (False)
(assert (not (not (= x 59632))))

(check-sat)
(get-model)
