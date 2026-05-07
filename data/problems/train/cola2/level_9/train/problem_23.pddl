

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b11)
(on b4 b8)
(ontable b5)
(on b6 b5)
(on b7 b4)
(ontable b8)
(on b9 b2)
(on b10 b6)
(ontable b11)
(clear b1)
(clear b3)
(clear b7)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b7)
(on b2 b3)
(on b3 b10)
(on b4 b2)
(on b7 b5)
(on b8 b1)
(on b9 b11)
(on b10 b6)
(on b11 b4))
)
)


