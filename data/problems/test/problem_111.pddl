

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b10)
(ontable b2)
(on b3 b4)
(ontable b4)
(on b5 b9)
(on b6 b5)
(on b7 b11)
(ontable b8)
(on b9 b1)
(ontable b10)
(on b11 b6)
(clear b2)
(clear b3)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b7)
(on b2 b5)
(on b3 b9)
(on b4 b2)
(on b6 b8)
(on b8 b3)
(on b9 b10)
(on b11 b4))
)
)


