

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on-table b1)
(on b2 b3)
(on b3 b9)
(on b4 b2)
(on b5 b1)
(on b6 b11)
(on-table b7)
(on b8 b5)
(on b9 b7)
(on-table b10)
(on-table b11)
(on b12 b6)
(clear b4)
(clear b8)
(clear b10)
(clear b12)
)
(:goal
(and
(on b2 b4)
(on b4 b10)
(on b5 b6)
(on b6 b9)
(on b7 b11)
(on b8 b12)
(on b10 b1)
(on b11 b2))
)
)


