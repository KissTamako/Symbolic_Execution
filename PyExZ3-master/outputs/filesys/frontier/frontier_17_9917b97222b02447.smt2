(set-logic ALL)
; Constraint ID: 9917b97222b02447
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59860)) (False)
(assert (not (= x 59860)))

; Query: ((== x 59861)) (False)
(assert (not (not (= x 59861))))

(check-sat)
(get-model)
