(set-logic ALL)
; Constraint ID: 1828898fbbe7d371
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60319)) (False)
(assert (not (= x 60319)))

; Query: ((== x 60320)) (False)
(assert (not (not (= x 60320))))

(check-sat)
(get-model)
