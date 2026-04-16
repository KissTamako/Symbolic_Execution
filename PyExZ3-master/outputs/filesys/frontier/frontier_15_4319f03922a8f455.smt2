(set-logic ALL)
; Constraint ID: 4319f03922a8f455
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60382)) (False)
(assert (not (= x 60382)))

; Query: ((== x 60383)) (False)
(assert (not (not (= x 60383))))

(check-sat)
(get-model)
