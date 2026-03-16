

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b8)
(ontable b3)
(ontable b4)
(on b5 b7)
(ontable b6)
(on b7 b11)
(on b8 b4)
(on b9 b3)
(on b10 b9)
(on b11 b2)
(clear b1)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b5)
(on b4 b11)
(on b5 b9)
(on b6 b10)
(on b8 b4)
(on b11 b6))
)
)


