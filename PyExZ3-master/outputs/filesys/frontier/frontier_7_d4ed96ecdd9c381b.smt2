(set-logic ALL)
; Constraint ID: d4ed96ecdd9c381b
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60145)) (False)
(assert (not (= x 60145)))

; Query: ((== x 60146)) (False)
(assert (not (not (= x 60146))))

(check-sat)
(get-model)
