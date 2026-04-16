(set-logic ALL)
; Constraint ID: eb323a4edb940f44
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59845)) (False)
(assert (not (= x 59845)))

; Query: ((== x 59846)) (False)
(assert (not (not (= x 59846))))

(check-sat)
(get-model)
