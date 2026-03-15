

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b7)
(on-table b2)
(on b3 b6)
(on b4 b8)
(on-table b5)
(on b6 b11)
(on b7 b10)
(on b8 b12)
(on-table b9)
(on-table b10)
(on b11 b9)
(on b12 b2)
(clear b1)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b3 b5)
(on b5 b8)
(on b6 b12)
(on b7 b4)
(on b8 b9)
(on b9 b6)
(on b10 b3)
(on b11 b7)
(on b12 b1))
)
)


