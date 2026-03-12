

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b9)
(on b3 b1)
(on-table b4)
(on b5 b2)
(on-table b6)
(on-table b7)
(on b8 b11)
(on b9 b7)
(on b10 b8)
(on-table b11)
(clear b3)
(clear b4)
(clear b6)
(clear b10)
)
(:goal
(and
(on b2 b4)
(on b4 b9)
(on b5 b8)
(on b6 b1)
(on b7 b11)
(on b10 b2)
(on b11 b6))
)
)


