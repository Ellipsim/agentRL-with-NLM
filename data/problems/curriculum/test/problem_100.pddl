

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b10)
(on-table b4)
(on-table b5)
(on b6 b2)
(on b7 b6)
(on b8 b5)
(on b9 b3)
(on b10 b4)
(on b11 b12)
(on-table b12)
(clear b1)
(clear b7)
(clear b8)
(clear b9)
(clear b11)
)
(:goal
(and
(on b1 b5)
(on b3 b10)
(on b4 b8)
(on b8 b11)
(on b9 b3)
(on b10 b12)
(on b11 b2)
(on b12 b4))
)
)


