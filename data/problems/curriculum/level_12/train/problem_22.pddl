

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b11)
(on b2 b6)
(on-table b3)
(on-table b4)
(on b5 b10)
(on b6 b13)
(on b7 b12)
(on b8 b1)
(on b9 b4)
(on-table b10)
(on-table b11)
(on b12 b2)
(on b13 b8)
(clear b3)
(clear b5)
(clear b7)
(clear b9)
)
(:goal
(and
(on b2 b9)
(on b3 b13)
(on b5 b2)
(on b6 b5)
(on b7 b12)
(on b8 b11)
(on b12 b1)
(on b13 b4))
)
)


