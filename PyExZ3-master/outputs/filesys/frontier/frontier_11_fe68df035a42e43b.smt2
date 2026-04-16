(set-logic ALL)
; Constraint ID: fe68df035a42e43b
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59401)) (False)
(assert (not (= x 59401)))

; Query: ((== x 59402)) (False)
(assert (not (not (= x 59402))))

(check-sat)
(get-model)
