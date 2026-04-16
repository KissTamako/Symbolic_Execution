(set-logic ALL)
; Constraint ID: df25e192bc88b182
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60469)) (False)
(assert (not (= x 60469)))

; Query: ((== x 60470)) (False)
(assert (not (not (= x 60470))))

(check-sat)
(get-model)
