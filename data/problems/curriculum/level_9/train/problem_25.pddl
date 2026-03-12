

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b5)
(on b3 b11)
(on b4 b9)
(on-table b5)
(on-table b6)
(on-table b7)
(on b8 b10)
(on b9 b8)
(on b10 b7)
(on-table b11)
(clear b1)
(clear b3)
(clear b4)
(clear b6)
)
(:goal
(and
(on b1 b10)
(on b2 b8)
(on b3 b5)
(on b4 b7)
(on b5 b6)
(on b6 b4)
(on b9 b3)
(on b10 b2))
)
)


