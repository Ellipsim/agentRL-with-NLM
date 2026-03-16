

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b9)
(ontable b3)
(ontable b4)
(on b5 b7)
(on b6 b3)
(on b7 b8)
(on b8 b11)
(on b9 b10)
(ontable b10)
(on b11 b1)
(clear b2)
(clear b5)
(clear b6)
)
(:goal
(and
(on b5 b10)
(on b6 b1)
(on b7 b8)
(on b8 b2)
(on b10 b11)
(on b11 b4))
)
)


