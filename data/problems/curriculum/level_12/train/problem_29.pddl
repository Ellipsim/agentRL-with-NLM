

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b13)
(on b3 b4)
(on b4 b6)
(on-table b5)
(on b6 b5)
(on b7 b3)
(on b8 b1)
(on b9 b2)
(on-table b10)
(on b11 b8)
(on b12 b11)
(on b13 b12)
(clear b9)
(clear b10)
)
(:goal
(and
(on b2 b1)
(on b4 b13)
(on b5 b3)
(on b6 b12)
(on b7 b6)
(on b10 b11)
(on b11 b8)
(on b12 b9))
)
)


